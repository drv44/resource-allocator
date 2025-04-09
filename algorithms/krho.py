# File: algorithms/krho.py
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

def red_fox_update(sol, num_resources):
    new_sol = sol.copy()
    for i in random.sample(range(len(sol)), random.randint(1, len(sol)//2)):
        new_sol[i] = random.randint(0, num_resources - 1)
    return new_sol

def kookaburra_update(sol, num_resources):
    new_sol = sol.copy()
    for i in range(len(sol)):
        if random.random() < 0.3:
            new_sol[i] = (sol[i] + random.choice([-1, 1])) % num_resources
    return new_sol

def combine_updates(orig, r1, r2, exec_times, costs, quality):
    candidates = [orig, r1, r2]
    fitnesses = [objective_function(c, exec_times, costs, quality, Q) for c in candidates]
    return candidates[np.argmin(fitnesses)]

def run_krho(num_jobs, num_resources, population_size, max_iterations):
    exec_times, costs, quality = generate_matrices(num_jobs, num_resources)
    population = [np.random.randint(0, num_resources, size=num_jobs) for _ in range(population_size)]
    best_sol, best_fit = None, float('inf')

    for _ in range(max_iterations):
        new_pop = []
        for sol in population:
            rf = red_fox_update(sol, num_resources)
            kook = kookaburra_update(sol, num_resources)
            new_sol = combine_updates(sol, rf, kook, exec_times, costs, quality)
            new_pop.append(new_sol)
            fit = objective_function(new_sol, exec_times, costs, quality, Q)
            if fit < best_fit:
                best_fit, best_sol = fit, new_sol.copy()
        population = new_pop

    return {
        'best_solution': best_sol.tolist(),
        'best_fitness': best_fit,
        'exec_times': exec_times.tolist(),
        'costs': costs.tolist(),
        'quality': quality.tolist()
    }
