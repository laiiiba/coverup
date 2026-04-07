from pathlib import Path

def make_project_name(project_path: str, module_name:str) -> str:
    package_name = Path(project_path).parts[1]
    module_suffix = module_name.split(".")[-1]

    final_name = f"{package_name}-{module_suffix}"

    return final_name