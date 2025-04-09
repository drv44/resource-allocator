import pandas as pd
import numpy as np
import time

from algorithms.ehjso import run_ehjso
from algorithms.krho import run_krho

# Parameters
num_runs = 10
num_jobs = 5
num_resources = 4
population_size = 10
max_iterations = 100

results = []

def run_and_record(algorithm_name, algorithm_func):
    for run in range(num_runs):
        start_time = time.time()
        result = algorithm_func(num_jobs, num_resources, population_size, max_iterations)
        end_time = time.time()

        fitness = result['best_fitness']
        makespan = max([result['exec_times'][i][res] for i, res in enumerate(result['best_solution'])])
        success = fitness < 100  # Example threshold for success

        results.append({
            'Algorithm': algorithm_name,
            'Run': run + 1,
            'Fitness': fitness,
            'Makespan': makespan,
            'ComputationTime': round(end_time - start_time, 4),
            'Success': int(success)
        })

# Run both algorithms
run_and_record("EHJSO", run_ehjso)
run_and_record("KRHO", run_krho)

# Save results
df = pd.DataFrame(results)
df.to_csv("results.csv", index=False)

print("✅ Results saved to results.csv")
