import numpy as np
import json
import csv
import os

# Load configuration from JSON file
with open('inputs/simulation_config.json', 'r') as f:
    config = json.load(f)

# Set the random seed for reproducibility
np.random.seed(config["seed"])

#Create a list to store all the simulation results
results = []
# loop through each scenario and simulation count in the configuration
for scenario in config["scenarios"]:
#run the simulation for each specified count
    for count in config["simulation_counts"]:
#Randomly generate ASN_missing values based on the binomial distribution
        ASN_missing = np.random.binomial(
            scenario["inputs"]["ASN_missing"]["n"],
            scenario["inputs"]["ASN_missing"]["p"],
            count
        )

#create an empty list to store the delays for this experiment
        delays = []
#loop through each ASN_missing value and calculate the corresponding delay based on the scenario's parameters starting from 1 to the number of ASN_missing values
        for nummer, ASN in enumerate(ASN_missing, start=1):
#if the ASN is missing, generate a delau using the gamma distribution with the specified shape and scale parameters from the scenario's inputs. Otherwise, generate a delay using the normal distribution with the specified mean and standard deviation from the scenario's inputs.
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
#store the generated delay in the delays list and append the results to the results list with the scenario name, simulation count, replication number, seed, ASN_missing value, and delay.
            delays.append(delay)
#store the results of this individual simulation in the results list, including the scenario name, simulation count, replication number, seed, ASN_missing value, and delay.
            results.append({
                "scenario": scenario["name"],
                "simulation_count": count,
                "replication": nummer,
                "seed": config["seed"],
                "ASN_missing": ASN,
                "delay": delay

            })
# print the number of simulations and their average delay
        print(f"Amount of delays: {count}")
        print(f"mean delays: {np.mean(delays):.2f} dagen")

#standard code for creating the results directory if it doesn't exist and writing the simulation results to a CSV file.
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