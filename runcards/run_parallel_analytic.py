"""
Python script to run multiple wmin fit of on the same data with different model dimensions.
"""
import yaml
import copy
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

PARAM_SCAN =  range(38, 51)
MAX_PARALLEL_JOBS = 25
TEMPLATE_CARD = "template_analytical_L1.yaml"

FIT_NAME = "250612_analytic_L1"


def run_fit_process(n_param):
    with open(TEMPLATE_CARD) as f:
        card = yaml.safe_load(f)

    new_card = copy.deepcopy(card)

    # adjust number of parameters
    new_card["wmin_settings"]["n_basis"] = n_param

    output_filename = f"{FIT_NAME}_Nw_{new_card['wmin_settings']['n_basis']}.yaml"

    with open(output_filename, 'w') as f:
        yaml.dump(new_card, f, default_flow_style=False)

    # Run the fitting process and wait until it's over
    fit_process = subprocess.Popen(["wmin", output_filename])
    fit_process.wait()

    print(f"Fit process for n_basis = {n_param} completed.")

# Use a ThreadPoolExecutor to manage parallel job execution
with ThreadPoolExecutor(max_workers=MAX_PARALLEL_JOBS) as executor:
    futures = [executor.submit(run_fit_process, n_param) for n_param in PARAM_SCAN]

    for future in as_completed(futures):
        future.result()  # Ensure exceptions are raised if any occurred in the threads
