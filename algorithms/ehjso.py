# File: algorithms/ehjso.py
import numpy as np
import random

# Set weights for objective function
alpha, beta, gamma, delta = 1.0, 0.5, 0.3, 2.0
Q = 80

def generate_matrices(num_jobs, num_resources):
    exec_times = np.random.randint(8, 21, size=(num_jobs, num_resources))
    costs = np.random.randint(4, 11, size=(num_jobs, num_resources))
    quality = np.random.randint(60, 101, size=(num_jobs, num_resources))
    return exec_times, costs, quality

def objective_function(sol, exec_times, costs, quality, Q):
    total_time = sum(exec_times[i, sol[i]] for i in range(len(sol)))
    max_time = max(exec_times[i, sol[i]] for i in range(len(sol)))
    total_cost = sum(costs[i, sol[i]] for i in range(len(sol)))
    quality_penalty = sum(((max(0, Q - quality[i, sol[i]]) / Q) ** 2) for i in range(len(sol)))
    return alpha * total_time + beta * max_time + gamma * total_cost + delta * quality_penalty

def cuckoo_update(sol, num_resources):
    new_sol = sol.copy()
    idx = random.randint(0, len(sol)-1)
    new_sol[idx] = random.randint(0, num_resources - 1)
    return new_sol

def gwo_update(sol, best, num_resources):
    new_sol = sol.copy()
    for i in range(len(sol)):
        if random.random() < 0.5:
            new_sol[i] = (sol[i] + best[i]) // 2 if abs(sol[i] - best[i]) <= 1 else random.randint(0, num_resources - 1)
    return new_sol

def combine_updates(orig, c1, c2, exec_times, costs, quality):
    candidates = [orig, c1, c2]
    fitnesses = [objective_function(c, exec_times, costs, quality, Q) for c in candidates]
    return candidates[np.argmin(fitnesses)]

def run_ehjso(num_jobs, num_resources, population_size, max_iterations):
    exec_times, costs, quality = generate_matrices(num_jobs, num_resources)
    population = [np.random.randint(0, num_resources, size=num_jobs) for _ in range(population_size)]
    best_sol = min(population, key=lambda sol: objective_function(sol, exec_times, costs, quality, Q))
    best_fit = objective_function(best_sol, exec_times, costs, quality, Q)

    for _ in range(max_iterations):
        new_pop = []
        for sol in population:
            cuckoo = cuckoo_update(sol, num_resources)
            gwo = gwo_update(sol, best_sol, num_resources)
            new_sol = combine_updates(sol, cuckoo, gwo, exec_times, costs, quality)
            new_pop.append(new_sol)
            fit = objective_function(new_sol, exec_times, costs, quality, Q)
            if fit < best_fit:
                best_fit = fit
                best_sol = new_sol.copy()
        population = new_pop

    return {
        'best_solution': best_sol.tolist(),
        'best_fitness': best_fit,
        'exec_times': exec_times.tolist(),
        'costs': costs.tolist(),
        'quality': quality.tolist()
    }
