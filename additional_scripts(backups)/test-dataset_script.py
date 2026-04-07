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

    package_index = cmd.index("--package-dir") + 1
    package_path = cmd[package_index]
    project_name = Path(package_path).parts[1]

    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name

    try:
        subprocess.run(cmd, env=env, timeout=600) #10 minute limit 
    except:
        print(f"{project_name} timed out (exceeded 10 minutes).")






#coverup test-apps/flutils2/flutils/setuputils/cfg.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/flutils/flutils/txtutils.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/httpie/httpie/output/formatters/colors.py --package-dir httpie --tests-dir tests --model gpt-4o --disable-polluting
#test-apps/flutils2,flutils.setuputils.cfg
#test-apps/flutils,flutils.txtutils
#test-apps/httpie,httpie.output.formatters.colors
