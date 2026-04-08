import subprocess
import os
from pathlib import Path

COMMANDS = [ #SPECIFY VERSION
    [ #will work (stable package)
        "coverup",
        "dataset/flutils-b64/flutils/codecs/b64.py",
        "--package-dir", "dataset/flutils-b64/flutils",
        "--tests-dir", "dataset/flutils-b64/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "dataset/cookiecutter-replay/cookiecutter/replay.py",
        "--package-dir", "dataset/cookiecutter-replay/cookiecutter",
        "--tests-dir", "dataset/cookiecutter-replay/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "dataset/youtube-dl-metadatafromtitle/youtube_dl/postprocessor/metadatafromtitle.py",
        "--package-dir", "dataset/youtube-dl-metadatafromtitle/youtube_dl",
        "--tests-dir", "dataset/youtube-dl-metadatafromtitle/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "dataset/typesystem-formats/typesystem/formats.py",
        "--package-dir", "dataset/typesystem-formats/typesystem",
        "--tests-dir", "dataset/typesystem-formats/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #will work (tested module before)
        "coverup",
        "dataset/flutils-cfg/flutils/setuputils/cfg.py",
        "--package-dir", "dataset/flutils-cfg/flutils",
        "--tests-dir", "dataset/flutils-cfg/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "dataset/ansible-facter/lib/ansible/module_utils/facts/other/facter.py",
        "--package-dir", "dataset/ansible-facter/lib/ansible",
        "--tests-dir", "dataset/ansible-facter/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "dataset/ansible-urls/lib/ansible/plugins/filter/urls.py",
        "--package-dir", "dataset/ansible-urls/lib/ansible",
        "--tests-dir", "dataset/ansible-urls/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "dataset/PySnooper-utils/pysnooper/utils.py",
        "--package-dir", "dataset/PySnooper-utils/pysnooper",
        "--tests-dir", "dataset/PySnooper-utils/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "dataset/ansible-color/lib/ansible/utils/color.py",
        "--package-dir", "dataset/ansible-color/lib/ansible",
        "--tests-dir", "dataset/ansible-color/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #issue-tried twice
        "coverup",
        "dataset/ansible-auto/lib/ansible/plugins/inventory/auto.py",
        "--package-dir", "dataset/ansible-auto/lib/ansible",
        "--tests-dir", "dataset/ansible-auto/coverup-tests",
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


'''test-apps/flutils,flutils.codecs.b64
test-apps/cookiecutter,cookiecutter.replay
test-apps/youtube-dl,youtube_dl.postprocessor.metadatafromtitle
test-apps/typesystem,typesystem.formats
test-apps/flutils,flutils.setuputils.cfg
test-apps/ansible/lib,ansible.module_utils.facts.other.facter
test-apps/ansible/lib,ansible.plugins.filter.urls
test-apps/PySnooper,pysnooper.utils
test-apps/ansible/lib,ansible.utils.color
test-apps/ansible/lib,ansible.plugins.inventory.auto'''

