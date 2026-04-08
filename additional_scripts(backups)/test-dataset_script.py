import subprocess
import os
from pathlib import Path

COMMANDS = [
    [
        "coverup",
        "test-apps/flutils2/flutils/setuputils/cfg.py",
        "--package-dir", "test-apps/flutils2/flutils",
        "--tests-dir", "test-apps/flutils2/coverup-tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
    [
        "coverup",
        "test-apps/flutils/flutils/txtutils.py",
        "--package-dir", "test-apps/flutils/flutils",
        "--tests-dir", "test-apps/flutils/coverup-tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
    [
        "coverup",
        "test-apps/httpie/httpie/output/formatters/colors.py",
        "--package-dir", "test-apps/httpie/httpie",
        "--tests-dir", "test-apps/httpie/coverup-tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
]

for cmd in COMMANDS:
    print(f"\nRunning: {' '.join(cmd)}", flush=True)

    #MODIFY FOR REAL SCRIPT. We probably want parts[0]. 
    package_index = cmd.index("--package-dir") + 1
    package_path = cmd[package_index]
    project_name = Path(package_path).parts[1]

    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    env["EXPERIMENT_ID"] = "test-exp-v2" #change for each script
    env["RESULTS_CSV"] = "results/experiment_results.csv" 

    try:
        subprocess.run(cmd, env=env, timeout=900, check = True) #15 minute limit 
    except subprocess.TimeoutExpired:
        print(f"{project_name} timed out (exceeded 15 minutes).")
    except subprocess.CalledProcessError as e:
        print(f"{project_name} failed with the return code {e.returncode}.")
    except Exception as e:
        print(f"{project_name} failed with an unexpected error : {e}")






#coverup test-apps/flutils2/flutils/setuputils/cfg.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/flutils/flutils/txtutils.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/httpie/httpie/output/formatters/colors.py --package-dir httpie --tests-dir tests --model gpt-4o --disable-polluting
#test-apps/flutils2,flutils.setuputils.cfg
#test-apps/flutils,flutils.txtutils
#test-apps/httpie,httpie.output.formatters.colors
