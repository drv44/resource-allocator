import streamlit as st
import time
import pandas as pd

from algorithms.ehjso import run_ehjso
from algorithms.krho import run_krho

st.set_page_config(page_title="Hybrid Scheduler", layout="centered")
st.title("Hybrid Job Scheduling Optimization")

st.write("""
This app allows you to choose between two hybrid optimization algorithms:
- **EHJSO** (Cuckoo + GWO)
- **KRHO** (Kookaburra + Red Fox)

Enter job scheduling parameters below and click **Optimize**.
""")

with st.form(key="opt_form"):
    num_jobs = st.number_input("Number of Jobs", min_value=1, value=5)
    num_resources = st.number_input("Number of Resources", min_value=1, value=4)
    population_size = st.slider("Population Size", min_value=5, max_value=50, value=10)
    max_iterations = st.slider("Max Iterations", min_value=10, max_value=500, value=100)
    algorithm = st.selectbox("Choose Optimization Algorithm", ["EHJSO", "KRHO"])

    submitted = st.form_submit_button("Optimize Schedule")

if submitted:
    st.info(f"Running {algorithm} optimizer...")
    start_time = time.time()

    if algorithm == "EHJSO":
        result = run_ehjso(num_jobs, num_resources, population_size, max_iterations)
    else:
        result = run_krho(num_jobs, num_resources, population_size, max_iterations)

    end_time = time.time()
    comp_time = round(end_time - start_time, 4)

    # Log results
    log_data = {
        "Algorithm": algorithm,
        "NumJobs": num_jobs,
        "NumResources": num_resources,
        "BestFitness": result['best_fitness'],
        "ComputationTime": comp_time,
        "BestSolution": result['best_solution']
    }

    st.success("Optimization Complete!")
    st.subheader("Optimized Resource Allocation")
    st.write("Each number represents the selected resource for that job:")
    st.code(result['best_solution'])

    st.subheader("Computation Time")
    st.write(f"{comp_time} seconds")

    st.subheader("Objective Function (Fitness) Value")
    st.write(result['best_fitness'])

    # Display matrices
    st.subheader("Execution Time Matrix")
    st.dataframe(pd.DataFrame(result['exec_times']))
    st.subheader("Cost Matrix")
    st.dataframe(pd.DataFrame(result['costs']))
    st.subheader("Quality Matrix")
    st.dataframe(pd.DataFrame(result['quality']))

    # Append to log file
    log_df = pd.DataFrame([log_data])
    try:
        prev_logs = pd.read_csv("frontend_log.csv")
        log_df = pd.concat([prev_logs, log_df], ignore_index=True)
    except FileNotFoundError:
        pass

    log_df.to_csv("frontend_log.csv", index=False)
    st.success("Logged optimization results to frontend_log.csv")
