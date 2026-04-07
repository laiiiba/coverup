from pathlib import Path
import csv
from radon.complexity import cc_rank, cc_visit
import random
import helper_funcs

project_root = Path("..")
cm_csv_path = project_root / "dataset" / "test-apps" / "cm_modules.csv"

complexity_output_path = project_root / "cm-dataset-setup" / "cm_modules_complexity_results.csv"
selection_output_path = project_root / "cm-dataset-setup" / "selected_cm_modules.csv"

def compute_complexities():
    '''use radon to compute cyclomatic complexity and classify into easy, medium, hard'''

    with complexity_output_path.open("w", newline = "", encoding = "utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["project_name", "project_path", "module", "max_complexity_number", "radon_rank", "complexity_level"])
    
        with cm_csv_path.open(newline = "", encoding = "utf-8") as f:
            reader = csv.reader(f)

            for project_path, module_name in reader:
                project_name = helper_funcs.make_project_name(project_path, module_name)
                module_file = module_name.replace(".", "/") + ".py"
                file_path = project_root / "dataset" / project_path / module_file

                if not file_path.exists():
                    continue

                module_code = file_path.read_text(encoding = "utf-8")
                results = cc_visit(module_code)

                max_complexity = max((result.complexity for result in results), default = 0)
                rank = cc_rank(max_complexity)

                if rank in {"A", "B"}:
                    complexity_level = "easy"
                elif rank in {"C", "D"}:
                    complexity_level = "medium"
                else:
                    complexity_level = "hard"

                writer.writerow([project_name, project_path, module_name, max_complexity, rank, complexity_level])

def select_modules():
    '''select a subset of easy, medium, hard modules'''

    easy = []
    medium = []
    hard = []

    with complexity_output_path.open(newline = "", encoding = "utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            level = row["complexity_level"]

            if level == "easy":
                easy.append(row)
            elif level == "medium":
                medium.append(row)
            else:
                hard.append(row)

        selections = (
            random.sample(easy, 10) +
            random.sample(medium, 10) +
            random.sample(hard, 10)
        )
    
        with selection_output_path.open("w", newline = "", encoding = "utf-8") as out:
            writer = csv.writer(out)

            for row in selections:
                writer.writerow([row["project_path"], row["module"]])
                #writer.writerow([row["project_path"], row["module"], row["complexity_level"]]) #to check it does the right thing

def main():
    compute_complexities()
    select_modules()

if __name__ == "__main__":
    main()
