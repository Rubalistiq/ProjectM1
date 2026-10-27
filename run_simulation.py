import numpy as np
import json
import csv
import os

with open('simulation_config.json', 'r') as f:
    config = json.load(f)

np.random.seed(config["seed"])

results = []
for scenario in config["scenarios"]:
    for count in config["simulation_counts"]:
        ASN_missing = np.random.binomial(
            scenario["inputs"]["ASN_missing"]["n"],
            scenario["inputs"]["ASN_missing"]["p"],
            count
        )

        delays = []

        for nummer, ASN in enumerate(ASN_missing, start=1):
            if ASN == 1:
                delay = np.random.gamma(
                    scenario["inputs"]["late_penalty"]["shape"],
                    scenario["inputs"]["late_penalty"]["scale"]
                )
            else:
                delay = np.random.normal(

                    scenario["inputs"]["normal_delay_variance"]["mean"],
                    scenario["inputs"]["normal_delay_variance"]["stddev"]                    
                )
            delays.append(delay)
            results.append({
                "scenario": scenario["name"],
                "simulation_count": count,
                "replication": nummer,
                "seed": config["seed"],
                "ASN_missing": ASN,
                "delay": delay

            })
        print(f"Amount of delays: {count}")
        print(f"mean delays: {np.mean(delays):.2f} dagen")


os.makedirs("results", exist_ok=True)
with open("results/simulation_output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "scenario",
        "simulation_count",
        "replication",
        "seed",
        "ASN_missing",
        "delay"
    ])
    writer.writeheader()
    writer.writerows(results)