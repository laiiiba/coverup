def main():
    overall_codecarbon = EmissionsTracker(project_name = 'coverup', experiment_id = 'overall', output_dir = 'overall_codecarbon_logs', log_level = 'error')
    overall_codecarbon.start()

    try:
        from collections import defaultdict
        import os

        global state
        args = parse_args()

        if not args.tests_dir.exists():
            print(f'Directory "{args.tests_dir}" does not exist. Please specify the correct one or create it.')
            return 1

        # add source dir to paths so that the module doesn't need to be installed to be worked on
        if args.add_to_pythonpath:
            add_to_pythonpath(args.src_base_dir)

        if args.prompt_for_tests:
            try:
                chatter = llm.Chatter(model=args.model)
                chatter.set_log_msg(lambda ctx, msg: log_write(args, ctx, msg))
                chatter.set_log_json(lambda ctx, j: log_write(args, ctx, json.dumps(j, indent=2)))
                chatter.set_signal_retry(lambda: state.inc_counter('R'))

                chatter.set_model_temperature(args.model_temperature)
                chatter.set_max_backoff(args.max_backoff)

                if args.rate_limit:
                    chatter.set_token_rate_limit((args.rate_limit, 60))

                extra_request_pars = {}
                if "ollama" in args.model:
                    extra_request_pars['api_base'] = args.ollama_api_base
                if args.model.startswith("bedrock/anthropic"):
                    extra_request_pars['anthropic_version'] = args.bedrock_anthropic_version
                chatter.set_extra_request_pars(extra_request_pars)

                prompter = prompter_registry[args.prompt](cmd_args=args)
                for f in prompter.get_functions():
                    chatter.add_function(f)

            except llm.ChatterError as e:
                print(e)
                return 1

            log_write(args, 'startup', f"Command: {' '.join(sys.argv)}")

            # --- (1) load or measure initial coverage, figure out segmentation ---

            if args.checkpoint and (state := State.load_checkpoint(args.checkpoint)):
                print("Continuing from checkpoint;  coverage: ", end='', flush=True)
                coverage = state.get_initial_coverage()
            else:
                if args.disable_polluting or args.disable_failing:
                    # check and clean up suite before measuring coverage
                    check_whole_suite(args)

                try:
                    print("MODIFIED Measuring coverage...  ", end='', flush=True) 
                    '''test if the local executable is running correctly with changes'''
                    coverage = measure_suite_coverage(tests_dir=args.tests_dir, source_dir=args.package_dir,
                                                      pytest_args=args.pytest_args,
                                                      isolate_tests=args.isolate_tests,
                                                      branch_coverage=args.branch_coverage,
                                                      trace=(print if args.debug else None))
                    state = State(coverage)

                except subprocess.CalledProcessError as e:
                    print("Error measuring coverage:\n" + str(e.stdout, 'UTF-8', errors='ignore'))
                    return 1

            print(summary_coverage(coverage, args.source_files))
            # TODO also show running coverage estimate

            chatter.set_add_cost(state.add_cost)

            segments = sorted(get_missing_coverage(state.get_initial_coverage(), line_limit=args.line_limit),
                              key=lambda seg: seg.missing_count(), reverse=True)

            # save initial coverage so we don't have to redo it next time
            if args.checkpoint:
                state.save_checkpoint(args.checkpoint)

            # --- (2) prompt for tests ---

            print(f"Prompting {args.model} for tests to increase coverage...")
            print("(in the following, G=good, F=failed, U=useless and R=retry)")

            async def work_segment(seg: CodeSegment) -> None:
                if await improve_coverage(args, chatter, prompter, seg):
                    # Only mark done if was able to complete (True return),
                    # so that it can be retried after installing any missing modules
                    state.mark_done(seg)

                if args.checkpoint:
                    state.save_checkpoint(args.checkpoint)
                progress.signal_one_completed()

            worklist = []
            seg_done_count = 0
            for seg in segments:
                if not seg.path.is_relative_to(args.src_base_dir):
                    continue

                if args.source_files and seg.path not in args.source_files:
                    continue

                if state.is_done(seg):
                    seg_done_count += 1
                else:
                    worklist.append(work_segment(seg))

            progress = Progress(total=len(worklist)+seg_done_count, initial=seg_done_count)
            state.set_progress_bar(progress)

            async def run_it():
                if args.max_concurrency:
                    semaphore = asyncio.Semaphore(args.max_concurrency)

                    async def sem_coro(coro):
                        async with semaphore:
                            return await coro

                    await asyncio.gather(*(sem_coro(c) for c in worklist))
                else:
                    await asyncio.gather(*worklist)

            try:
                asyncio.run(run_it())
            except KeyboardInterrupt:
                print("Interrupted.")
                if args.checkpoint:
                    state.save_checkpoint(args.checkpoint)
                return 1

            progress.close()

        # --- (3) clean up resulting test suite ---

        if args.disable_polluting or args.disable_failing:
            check_whole_suite(args)

        # --- (4) show final coverage

        if args.prompt_for_tests:
            try:
                print("MODIFIED Measuring coverage...  ", end='', flush=True)
                coverage = measure_suite_coverage(tests_dir=args.tests_dir, source_dir=args.package_dir,
                                                  pytest_args=args.pytest_args,
                                                  isolate_tests=args.isolate_tests,
                                                  branch_coverage=args.branch_coverage,
                                                  trace=(print if args.debug else None))

            except subprocess.CalledProcessError as e:
                print("Error measuring coverage:\n" + str(e.stdout, 'UTF-8', errors='ignore'))
                return 1

            print(summary_coverage(coverage, args.source_files))

        # --- (5) save state and show missing modules, if appropriate

            if args.checkpoint:
                state.set_final_coverage(coverage)
                state.save_checkpoint(args.checkpoint)

            if not args.install_missing_modules and (required := get_required_modules()):
                print(f"Some modules seem to be missing:  {', '.join(str(m) for m in required)}")
                if args.write_requirements_to:
                    with args.write_requirements_to.open("a") as f:
                        for module in required:
                            f.write(f"{module}\n")
    
    finally: 
        overall_emissions = overall_codecarbon.stop()
        print(f"\nTotal CO2 emissions for overall process: {overall_emissions} kg", flush=True)

    return 0
