"""
Script to run multiple wmin fits on the same data with different model dimensions.
"""
import os
import pathlib
import sys
import yaml
import copy
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

FIT_NAME = "250612_disonly_L1"
MAX_PARALLEL_JOBS = 50
TEMPLATE_CARD = "template_numerical_L1.yaml"
PRIOR_FITS_DIR = pathlib.Path("") # NOTE: set path to where analytical fits are stored

PARAM_SCAN = [45, 60] #range(38, 51)

PRIOR_FITS_NAMES = [
    f"250612_analytic_L1_Nw_{nwgt}" for nwgt in PARAM_SCAN
]

# make sure that prior fits are available in colibri, create soft link of fit in fit_path
for fit in PRIOR_FITS_NAMES:

    fit_path = pathlib.Path(sys.prefix) / "share/colibri/results" / fit
    source_path = PRIOR_FITS_DIR / fit
    
    if not fit_path.exists():
        if source_path.exists():
            os.symlink(source_path, fit_path)
            print(f"Created symlink for {fit} at {fit_path}")
        else:
            print(f"Source fit {source_path} does not exist.")
    

def run_fit_process(prior_fit_name):

    # open prior fit runcard
    with open(PRIOR_FITS_DIR / prior_fit_name / "filter.yml") as f:
        prior_card = yaml.safe_load(f)
    
    level1_seed = prior_card["level_1_seed"]
    n_basis = prior_card["wmin_settings"]["n_basis"]

    # open numerical fit template_card
    with open(TEMPLATE_CARD) as f:
        card = yaml.safe_load(f)

    new_card = copy.deepcopy(card)

    # numerical fit has as many parameters as prior analytical fit
    new_card["wmin_settings"]["n_basis"] = n_basis
    # ensure same basis is used in fit
    new_card["wmin_settings"]["wminpdfset"] = prior_card["wmin_settings"]["wminpdfset"]

    # set prior fit
    new_card["prior_settings"]["prior_distribution_specs"]["prior_fit"] = prior_fit_name

    # Slice sampler settings: slice sampler does 2 * n_basis steps
    new_card["ns_settings"]["SliceSampler_settings"]["nsteps"] = 10 + int(
        3 * prior_card["wmin_settings"]["n_basis"]
    )

    # set the random L1 seed
    new_card["level_1_seed"] = level1_seed
    new_card["closuretest"]["filterseed"] = level1_seed  # needed for validphys reports

    output_filename = f"{FIT_NAME}_Nw_{n_basis}.yaml"

    with open(output_filename, "w") as f:
        yaml.dump(new_card, f, default_flow_style=False)

    # Run the fitting process and wait until it's over
    fit_process = subprocess.Popen(["wmin", output_filename])
    fit_process.wait()

    print(
        f"Fit process for n_basis, fs = {prior_card['wmin_settings']['n_basis'], level1_seed} completed."
    )


# Use a ThreadPoolExecutor to manage parallel job execution
with ThreadPoolExecutor(max_workers=MAX_PARALLEL_JOBS) as executor:
    futures = [
        executor.submit(run_fit_process, prior_fit_name)
        for prior_fit_name in PRIOR_FITS_NAMES
    ]

    for future in as_completed(futures):
        future.result()  # Ensure exceptions are raised if any occurred in the threads
