    async def _send_request(self, request: dict, ctx: object) -> litellm.ModelResponse | None:
        """Sends the LLM chat request, handling common failures and returning the response."""

        project_name = os.environ.get("PROJECT_NAME", "unknown")
        llm_call_codecarbon = EmissionsTracker(project_name = project_name, experiment_id = 'llm_call', log_level = 'error')
        llm_call_codecarbon.start()

        try:
            sleep = 1
            while True:
                try:
                    # TODO also add request limit; could use 'await asyncio.gather(t.acquire(tokens), r.acquire())'
                    # # to acquire both
                    if self.token_rate_limit:
                        try:
                            await asyncio.wait_for(self.token_rate_limit.acquire(count_tokens(self._model, request)), timeout = 300) #5 minute timeout
                        except asyncio.TimeoutError:
                            self._log_msg(ctx, "Token rate limit acquire timed out after 5 minutes.")
                            return None 
                        except ValueError as e:
                            self._log_msg(ctx, f"Error: too many tokens for rate limit ({e})")
                            return None # gives up this segment
                    
                    try:
                        response = await asyncio.wait_for(litellm.acreate(**request), timeout = 300) #5 minute timeout
                    except asyncio.TimeoutError:
                        self._log_msg(ctx, "LLM call timed out after 5 minutes.")
                        return None 

                    ecologits_codecarbon = EmissionsTracker(project_name = project_name, experiment_id = 'ecologits', log_level = 'error')
                    ecologits_codecarbon.start()

                    try: 
                        time_of_log = datetime.now().isoformat(timespec='seconds')
                        energy = response.impacts.energy
                        min_energy = energy.value.min
                        max_energy = energy.value.max
                        mid_energy = (min_energy + max_energy)/2
                        energy_unit = energy.unit 
                        '''consider using nowtricity instead'''
                        gwp = response.impacts.gwp
                        min_emissions = gwp.value.min
                        max_emissions = gwp.value.max
                        mid_emissions = (min_emissions + max_emissions)/2
                        emissions_unit = gwp.unit

                        file_path = "ecologits_impacts.csv"
                        file_exists = os.path.isfile(file_path)

                        with open(file_path, mode="a", newline="") as f:
                            writer = csv.writer(f)
                            if not file_exists:
                                writer.writerow(["time","project name","energy min", "energy max", "energy midpoint", "energy unit", "emissions min", "emissions max", "emissions midpoint", "emissions unit"])
                            writer.writerow([time_of_log, project_name, min_energy, max_energy, mid_energy, energy_unit, min_emissions, max_emissions, mid_emissions, emissions_unit])
                    
                        #print(f"\nTotal (estimated) server side CO2 emissions for LLM call: {mid_emissions} kgCO2eq", flush=True)
                
                    except Exception as e:
                        print(f"Failed to log energy: {e}")
                    
                    ecologits_codecarbon.stop()
                
                    return response           

                except (litellm.exceptions.ServiceUnavailableError,
                        openai.RateLimitError,
                        openai.APITimeoutError) as e:

                    # This message usually indicates out of money in account
                    if 'You exceeded your current quota' in str(e):
                        self._log_msg(ctx, f"Failed: {type(e)} {e}")
                        raise

                    import random
                    sleep = min(sleep * 2, self._max_backoff)
                    sleep_time = random.uniform(sleep / 2, sleep)

                    self._log_msg(ctx, f"Error: {type(e)} {e} {sleep=} {sleep_time=}")

                    self._signal_retry()
                    await asyncio.sleep(sleep_time)

                except openai.BadRequestError as e:
                    # usually "maximum context length" XXX check for this?
                    self._log_msg(ctx, f"Error: {type(e)} {e}")
                    return None # gives up this segment

                except openai.AuthenticationError as e:
                    self._log_msg(ctx, f"Failed: {type(e)} {e}")
                    raise

                except openai.APIConnectionError as e:
                    self._log_msg(ctx, f"Error: {type(e)} {e}")
                    # usually a server-side error... just retry right away
                    self._signal_retry()

                except openai.APIError as e:
                    # APIError is the base class for all API errors;
                    # we may be missing a more specific handler.
                    print(f"Error: {type(e)} {e}; missing handler?")
                    self._log_msg(ctx, f"Error: {type(e)} {e}")
                    return None # gives up this segment
        finally:
            llm_call_codecarbon.stop()
            #llm_call_emissions = llm_call_codecarbon.stop()
            #print(f"\nTotal client side CO2 emissions for llm call: {llm_call_emissions-ecologits_emissions} kgCO2eq", flush=True)