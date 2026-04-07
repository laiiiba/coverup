from pathlib import Path
import tempfile
import subprocess
import pytest
import typing as T
import sys
import json
import os
import re
from .utils import subprocess_run
from codecarbon import EmissionsTracker


async def measure_test_coverage(*, test: str, tests_dir: Path, pytest_args='',
                                log_write=None, isolate_tests=False, branch_coverage=True):
    """Runs a given test and returns the coverage obtained."""
    with tempfile.NamedTemporaryFile(prefix="tmp_test_", suffix='.py', dir=str(tests_dir), mode="w") as t:
        t.write(test)
        t.flush()

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as j:
            try:
                # -qq to cut down on tokens
                p = await subprocess_run([sys.executable, '-m', 'slipcover',  *(('--branch',) if branch_coverage else ()),
                                          '--json', '--out', j.name,
                                          '-m', 'pytest', *pytest_args.split(),
                                          *(('--isolate',) if isolate_tests else ()),
                                          '-qq', '-x', '--disable-warnings', t.name],
                                         check=True, timeout=60)
                if log_write:
                    log_write(str(p.stdout, 'UTF-8', errors='ignore'))

                # not checking for JSON errors here because if pytest aborts, its RC ought to be !=0
                cov = json.load(j)
            finally:
                j.close()
                try:
                    os.unlink(j.name)
                except FileNotFoundError:
                    pass

    return cov

def measure_suite_coverage(*, tests_dir: Path, source_dir: T.Optional[Path], pytest_args='',
                           trace=None, isolate_tests=False, branch_coverage=True):
    """Runs an entire test suite and returns the coverage obtained."""
    
    project_name = os.environ.get("PROJECT_NAME", "unknown")
    suite_coverage_codecarbon = EmissionsTracker(project_name = project_name, experiment_id = 'suite_coverage', log_level = 'error')
    suite_coverage_codecarbon.start()
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as j:
            try:
                command = [sys.executable,
                           '-m', 'slipcover',
                           *(('--source', source_dir) if source_dir else ()),
                           *(('--branch',) if branch_coverage else ()),
                           '--json', '--out', j.name,
                           '-m', 'pytest', *pytest_args.split(), *(('--isolate',) if isolate_tests else ()),
                           '--disable-warnings', '-x', tests_dir]
                
                if trace: trace(command)
                p = subprocess.run(command, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if p.returncode not in (pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED):
                    if trace: trace(f"tests rc={p.returncode}\n" + str(p.stdout, 'utf-8'))
                    p.check_returncode()
                
                try:
                    return json.load(j)
                except json.decoder.JSONDecodeError:
                    # The JSON is broken, so pytest's execution likely aborted (e.g. a Python unhandled exception).
                    p.check_returncode() # this will almost certainly raise an exception. If not, we do it ourselves:
                    raise subprocess.CalledProcessError(p.returncode, command, output=p.stdout)
            finally:
                j.close()
                
                try:
                    os.unlink(j.name)
                except FileNotFoundError:
                    pass

    finally:
        suite_coverage_emissions = suite_coverage_codecarbon.stop()
        print(f"\nTotal CO2 emissions for suite coverage: {suite_coverage_emissions} kgCO2eq", flush=True)


def measure_suite_mutation_score(*, project_dir: Path, trace=None) -> float:
    """Runs mutation tests and returns the mutation score."""

    try:
        run_command = ["mutmut", "run"]
        if trace: 
            trace(run_command)
    
        run_result = subprocess.run(run_command, cwd = project_dir, check = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, text = True)

        output = run_result.stdout
        
        matches = re.findall(r"🎉\s*(\d+).*🫥\s*(\d+)", output)
        if not matches:
            print("Could not obtain results from mutmut output.")
            print(output)
            return None 
        
        last_match = matches[-1]
        killed_mutants = int(last_match[0])
        survived_mutants = int(last_match[1])

        total_mutants = killed_mutants + survived_mutants

        if total_mutants > 0:
            mutation_score = killed_mutants / total_mutants
        else:
            mutation_score = 0.0

        return mutation_score

    except Exception as e:
        print("Cannot obtain mutation results:", e)
        return None 





