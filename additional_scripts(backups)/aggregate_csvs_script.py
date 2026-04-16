import pandas as pd 

ecologits = pd.read_csv("ecologits_impacts.csv")
cc = pd.read_csv("emissions.csv")
results = pd.read_csv("results/experiment_results.csv")#change to proper path 

#ecologits
#ecologits aggregation
ecologits_agg = ecologits.groupby("project_name").agg({
    "energy_midpoint": "sum",
    "emissions_midpoint": "sum"
}).reset_index()

ecologits_agg.rename(columns={
    "energy_midpoint": "ecologits_energy",
    "emissions_midpoint": "ecologits_emissions"
}, inplace=True)

#codecarbon
#cc["emissions"] = cc["emissions"].fillna(0)

#codecarbon aggregation
cc_grouped = cc.groupby(["project_name", "experiment_id"])["emissions"].sum(min_count=1).reset_index()

cc_pivot = cc_grouped.pivot(
    index = "project_name",
    columns = "experiment_id",
    values = "emissions"
)

cc_pivot = cc_pivot.add_prefix("cc_").add_suffix("_emissions")

#subtract ecologits instrumentation cc from llm_call_cc, remove ecologits_cc column
if "cc_llm_call_emissions" in cc_pivot.columns and "cc_ecologits_emissions" in cc_pivot.columns:
    cc_pivot["cc_llm_call_emissions"] = cc_pivot["cc_llm_call_emissions"] - cc_pivot["cc_ecologits_emissions"].fillna(0)
    cc_pivot["cc_llm_call_emissions"] = cc_pivot["cc_llm_call_emissions"].clip(lower=0)
    cc_pivot = cc_pivot.drop(columns = ["cc_ecologits_emissions"])

stage_columns = [col for col in cc_pivot.columns if col != "cc_overall_emissions"]
cc_pivot["cc_sum_of_stages_emissions"] = cc_pivot[stage_columns].sum(axis=1, min_count=1)

cc_final = cc_pivot.reset_index()

final = ecologits_agg.merge(cc_final, on="project_name", how="outer") \
    .merge(results, on="project_name", how="outer")

#final["ecologits_energy"] = final["ecologits_energy"].fillna(0)
#final["ecologits_emissions"] = final["ecologits_emissions"].fillna(0)

#cc_columns = [col for col in final.columns if col.startswith("cc_")]
#final[cc_columns] = final[cc_columns].fillna(0)

#fill in experiment_id using existing value
existing_experiments_ids = final["experiment_id"].dropna().unique()

if len(existing_experiments_ids) == 1:
    final["experiment_id"] = final["experiment_id"].fillna(existing_experiments_ids[0])
elif len() == 0:
    print("warning: no existing experiment_id found to fill missing values")
else:
    print("warning: multiple experiment_id values found", existing_experiments_ids)

final["status"] = final["status"].fillna("timeout")
final.to_csv("aggregated_results.csv", index=False)

#checks
print(final.shape)
print(final["project_name"].nunique())
print(final.head())