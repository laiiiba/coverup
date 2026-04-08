import subprocess
import os
from pathlib import Path

COMMANDS = [ #SPECIFY VERSION
    [ #will work (stable package)
        "coverup",
        "flutils-b64/flutils/codecs/b64.py",
        "--package-dir", "flutils-b64/flutils",
        "--tests-dir", "flutils-b64/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "cookiecutter-replay/cookiecutter/replay.py",
        "--package-dir", "cookiecutter-replay/cookiecutter",
        "--tests-dir", "cookiecutter-replay/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "youtube-dl-metadatafromtitle/youtube_dl/postprocessor/metadatafromtitle.py",
        "--package-dir", "youtube-dl-metadatafromtitle/youtube_dl",
        "--tests-dir", "youtube-dl-metadatafromtitle/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #works
        "coverup",
        "typesystem-formats/typesystem/formats.py",
        "--package-dir", "typesystem-formats/typesystem",
        "--tests-dir", "typesystem-formats/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #will work (tested module before)
        "coverup",
        "flutils-cfg/flutils/setuputils/cfg.py",
        "--package-dir", "flutils-cfg/flutils",
        "--tests-dir", "flutils-cfg/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "ansible-facter/lib/ansible/module_utils/facts/other/facter.py",
        "--package-dir", "ansible-facter/lib/ansible",
        "--tests-dir", "ansible-facter/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "ansible-urls/lib/ansible/plugins/filter/urls.py",
        "--package-dir", "ansible-urls/lib/ansible",
        "--tests-dir", "ansible-urls/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "PySnooper-utils/pysnooper/utils.py",
        "--package-dir", "PySnooper-utils/pysnooper",
        "--tests-dir", "PySnooper-utils/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #works
        "coverup",
        "ansible-color/lib/ansible/utils/color.py",
        "--package-dir", "ansible-color/lib/ansible",
        "--tests-dir", "ansible-color/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #issue-tried twice
        "coverup",
        "ansible-auto/lib/ansible/plugins/inventory/auto.py",
        "--package-dir", "ansible-auto/lib/ansible",
        "--tests-dir", "ansible-auto/coverup-tests",
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
    project_name = Path(package_path).parts[0]

    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    env["EXPERIMENT_ID"] = "baseline-v2" #change for each script
    env["RESULTS_CSV"] = "results/experiment_results.csv" 

    try:
        subprocess.run(cmd, env=env, timeout=900) #15 minute limit 
    except:
        print(f"{project_name} timed out (exceeded 15 minutes).")


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

