import subprocess
import os
from pathlib import Path

COMMANDS = [ #SPECIFY VERSION
    [ #
        "coverup",
        "dataset/ansible-debug/lib/ansible/plugins/action/debug.py",
        "--package-dir", "dataset/ansible-debug/lib/ansible",
        "--tests-dir", "dataset/ansible-debug/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-clean/lib/ansible/vars/clean.py",
        "--package-dir", "dataset/ansible-clean/lib/ansible",
        "--tests-dir", "dataset/ansible-clean/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-context_objects/lib/ansible/utils/context_objects.py",
        "--package-dir", "dataset/ansible-context_objects/lib/ansible",
        "--tests-dir", "dataset/ansible-context_objects/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-getent/lib/ansible/modules/getent.py",
        "--package-dir", "dataset/ansible-getent/lib/ansible",
        "--tests-dir", "dataset/ansible-getent/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-psrp/lib/ansible/plugins/connection/psrp.py",
        "--package-dir", "dataset/ansible-psrp/lib/ansible",
        "--tests-dir", "dataset/ansible-psrp/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-hpux/lib/ansible/module_utils/facts/hardware/hpux.py",
        "--package-dir", "dataset/ansible-hpux/lib/ansible",
        "--tests-dir", "dataset/ansible-hpux/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-task/lib/ansible/playbook/task.py",
        "--package-dir", "dataset/ansible-task/lib/ansible",
        "--tests-dir", "dataset/ansible-task/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #will work (tested module before)
        "coverup",
        "dataset/flutils-pathutils/flutils/pathutils.py",
        "--package-dir", "dataset/flutils-pathutils/flutils",
        "--tests-dir", "dataset/flutils-pathutils/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/dataclasses-json-core/dataclasses_json/core.py",
        "--package-dir", "dataset/dataclasses-json-core/dataclasses_json",
        "--tests-dir", "dataset/dataclasses-json-core/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-conditional/lib/ansible/playbook/conditional.py",
        "--package-dir", "dataset/ansible-conditional/lib/ansible",
        "--tests-dir", "dataset/ansible-conditional/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
]

for cmd in COMMANDS:
    print(f"\nRunning: {' '.join(cmd)}", flush=True)

    package_index = cmd.index("--package-dir") + 1
    package_path = cmd[package_index]
    project_name = Path(package_path).parts[1]

    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    env["EXPERIMENT_ID"] = "baseline-v2" #change for each script
    env["RESULTS_CSV"] = "results/experiment_results.csv" 

    try:
        subprocess.run(cmd, env=env, timeout=900, check=True) #15 minute limit 
    except subprocess.TimeoutExpired:
        print(f"{project_name} timed out (exceeded 15 minutes).")
    except subprocess.CalledProcessError as e:
        print(f"{project_name} failed with the return code {e.returncode}.")
    except Exception as e:
        print(f"{project_name} failed with an unexpected error : {e}")


'''test-apps/ansible/lib,ansible.plugins.action.debug
test-apps/ansible/lib,ansible.vars.clean
test-apps/ansible/lib,ansible.utils.context_objects
test-apps/ansible/lib,ansible.modules.getent
test-apps/ansible/lib,ansible.plugins.connection.psrp
test-apps/ansible/lib,ansible.module_utils.facts.hardware.hpux
test-apps/ansible/lib,ansible.playbook.task
test-apps/flutils,flutils.pathutils
test-apps/dataclasses-json,dataclasses_json.core
test-apps/ansible/lib,ansible.playbook.conditional'''

