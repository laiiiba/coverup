import pandas as pd
import glob

files = glob.glob("*/aggregated_results.csv")

data = [pd.read_csv(f) for f in files]

combined = pd.concat(data, ignore_index = True)

complexity = pd.read_csv("../cm-dataset-setup/cm_modules_complexity_results.csv")

combined = combined.merge(
    complexity[[
        "project_name",
        "max_complexity_number",
        "radon_rank",
        "complexity_level"
    ]],
    on="project_name",
    how="left"
)

combined.to_csv("../experiment-results/all_experiments.csv", index=False)

