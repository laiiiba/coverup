import pandas as pd
import glob

files = glob.glob("*/aggregated_results.csv")

data = [pd.read_csv(f) for f in files]

combined = pd.concat(data, ignore_index = True)

combined.to_csv("../experiment-results/all_experiments.csv", index=False)