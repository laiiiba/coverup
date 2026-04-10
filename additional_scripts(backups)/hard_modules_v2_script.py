import subprocess
import os
from pathlib import Path

COMMANDS = [ #SPECIFY VERSION
    [ #
        "coverup",
        "dataset/ansible-linear/lib/ansible/plugins/strategy/linear.py",
        "--package-dir", "dataset/ansible-linear/lib/ansible",
        "--tests-dir", "dataset/ansible-linear/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-sunos/lib/ansible/module_utils/facts/virtual/sunos.py",
        "--package-dir", "dataset/ansible-sunos/lib/ansible",
        "--tests-dir", "dataset/ansible-sunos/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-systemd/lib/ansible/modules/systemd.py",
        "--package-dir", "dataset/ansible-systemd/lib/ansible",
        "--tests-dir", "dataset/ansible-systemd/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],
    [ #
        "coverup",
        "dataset/ansible-lineinfile/lib/ansible/modules/lineinfile.py",
        "--package-dir", "dataset/ansible-lineinfile/lib/ansible",
        "--tests-dir", "dataset/ansible-lineinfile/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/tornado-simple_httpclient/tornado/simple_httpclient.py",
        "--package-dir", "dataset/tornado-simple_httpclient/tornado",
        "--tests-dir", "dataset/tornado-simple_httpclient/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-splitter/lib/ansible/parsing/splitter.py",
        "--package-dir", "dataset/ansible-splitter/lib/ansible",
        "--tests-dir", "dataset/ansible-splitter/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],   
    [ #
        "coverup",
        "dataset/youtube-dl-swfinterp/youtube_dl/swfinterp.py",
        "--package-dir", "dataset/youtube-dl-swfinterp/youtube_dl",
        "--tests-dir", "dataset/youtube-dl-swfinterp/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],  
    [ #
        "coverup",
        "dataset/typesystem-fields/typesystem/fields.py",
        "--package-dir", "dataset/typesystem-fields/typesystem",
        "--tests-dir", "dataset/typesystem-fields/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],       
    [ #
        "coverup",
        "dataset/ansible-play_iterator/lib/ansible/executor/play_iterator.py",
        "--package-dir", "dataset/ansible-play_iterator/lib/ansible",
        "--tests-dir", "dataset/ansible-play_iterator/coverup-tests",
        "--model", "gpt-4o",
        "--prompt", "gpt-v2",
        "--disable-failing",
        "--install-missing-modules",
    ],    
    [ #
        "coverup",
        "dataset/ansible-play_context/lib/ansible/playbook/play_context.py",
        "--package-dir", "dataset/ansible-play_context/lib/ansible",
        "--tests-dir", "dataset/ansible-play_context/coverup-tests",
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


'''test-apps/ansible/lib,ansible.plugins.strategy.linear
test-apps/ansible/lib,ansible.module_utils.facts.virtual.sunos
test-apps/ansible/lib,ansible.modules.systemd
test-apps/ansible/lib,ansible.modules.lineinfile
test-apps/tornado,tornado.simple_httpclient
test-apps/ansible/lib,ansible.parsing.splitter
test-apps/youtube-dl,youtube_dl.swfinterp
test-apps/typesystem,typesystem.fields
test-apps/ansible/lib,ansible.executor.play_iterator
test-apps/ansible/lib,ansible.playbook.play_context'''

