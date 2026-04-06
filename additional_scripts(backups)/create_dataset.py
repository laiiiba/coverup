import shutil
from pathlib import Path

input_modules = [
    "test-apps/flutils,flutils.codecs.b64",
    "test-apps/cookiecutter,cookiecutter.replay",
    "test-apps/youtube-dl,youtube_dl.postprocessor.metadatafromtitle",
    "test-apps/typesystem,typesystem.formats",
    "test-apps/flutils,flutils.setuputils.cfg",
    "test-apps/ansible/lib,ansible.module_utils.facts.other.facter",
    "test-apps/ansible/lib,ansible.plugins.filter.urls",
    "test-apps/PySnooper,pysnooper.utils",
    "test-apps/ansible/lib,ansible.utils.color",
    "test-apps/ansible/lib,ansible.plugins.inventory.auto",
    "test-apps/ansible/lib,ansible.plugins.action.debug",
    "test-apps/ansible/lib,ansible.vars.clean",
    "test-apps/ansible/lib,ansible.utils.context_objects",
    "test-apps/ansible/lib,ansible.modules.getent",
    "test-apps/ansible/lib,ansible.plugins.connection.psrp",
    "test-apps/ansible/lib,ansible.module_utils.facts.hardware.hpux",
    "test-apps/ansible/lib,ansible.playbook.task",
    "test-apps/flutils,flutils.pathutils",
    "test-apps/dataclasses-json,dataclasses_json.core",
    "test-apps/ansible/lib,ansible.playbook.conditional",
    "test-apps/ansible/lib,ansible.plugins.strategy.linear",
    "test-apps/ansible/lib,ansible.module_utils.facts.virtual.sunos",
    "test-apps/ansible/lib,ansible.modules.systemd",
    "test-apps/ansible/lib,ansible.modules.lineinfile",
    "test-apps/tornado,tornado.simple_httpclient",
    "test-apps/ansible/lib,ansible.parsing.splitter",
    "test-apps/youtube-dl,youtube_dl.swfinterp",
    "test-apps/typesystem,typesystem.fields",
    "test-apps/ansible/lib,ansible.executor.play_iterator",
    "test-apps/ansible/lib,ansible.playbook.play_context"
]

project_root = Path("..")
dataset_root = project_root / "dataset"
output_root = project_root / "cm-dataset-setup" / "final-dataset"

if output_root.exists():
    shutil.rmtree(output_root)

output_root.mkdir(parents=True, exist_ok=True)

for module in input_modules:
    package_path, module = module.strip().split(",")
    package_name = Path(package_path).parts[1]
    module_suffix = module.split(".")[-1]

    final_name = f"{package_name}-{module_suffix}"

    source = dataset_root / package_path
    dest = output_root / final_name

    if not source.exists():
        print(f"missing source: {source}")
        continue

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(source, dest)
    (dest / "coverup-tests").mkdir()