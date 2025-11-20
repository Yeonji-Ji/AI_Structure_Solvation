import os
import time
import subprocess
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed


start = time.time()

#####################################################
# Integration (target × structure × block × volume) #
#####################################################

targets = ["wee1"]
structures = ["xtal"]
blocks = ["80_100"]
volumes = [f"{v:.1f}" for v in np.arange(3.0, 10.5, 0.5)]
# base directory
base_path = f"/gibbs/yeonji/34_DUDE/"
# available CPU cores
N_CPU = os.cpu_count()

### Functions ###
def run_cmd(cmd: str):
    """Run a gistpp command."""
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_sum(dx_file: str) -> str:
    """Run `gistpp -op sum` and extract only the numeric result."""
    cmd = f"gistpp -i {dx_file} -op sum"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    try:
        return result.stdout.split("\n")[0].split(": ")[2]
    except Exception:
        return "NaN"


### Computation ###
def run_gist_combination(target, structure, blck, volumes, base_path):
    """
    Run all volume calculations for one (target, structure, block) combination,
    and save results to a CSV file.
    """
    # working directories (Change these)
    folder_name = f"{structure}_{blck}"
    inpath = f"{base_path}/{target.upper()}/{structure}/gistpp/{blck}/"
    outpath = os.path.join(inpath, "integration")
    gist_path = f"{base_path}/{target.upper()}/{structure}/gist/{blck}/"

    os.makedirs(outpath, exist_ok=True)
    os.chdir(outpath)

    # ligand file (Change these)
    lig = f"{base_path}/{target.upper()}/wee1_lig_aligned_to_avg.pdb"

    # Input data files
    data_paths = {
        "Etot": os.path.join(inpath, "Gist4-Etot.dx"),
        "grho": os.path.join(inpath, "grho.dx"),
        "Esw": os.path.join(inpath, "Gist4-Esw.dx"),
        "Eww": os.path.join(inpath, "Gist4-Eww.dx"),
        "Nsw_acc": os.path.join(gist_path, "Gist4-swacceptor-dens.dx"),
        "Nsw_don": os.path.join(gist_path, "Gist4-swdonor-dens.dx"),
        "Nww_acc": os.path.join(gist_path, "Gist4-wwacceptor-dens.dx"),
        "Nww_don": os.path.join(gist_path, "Gist4-wwdonor-dens.dx"),
    }

    ### Start calculations ###
    results = {}

    for vol in volumes:
        bp_out = f"{target}_{structure}_{blck}_bp{vol}.dx"
        gO_file = os.path.join(gist_path, "Gist4-gO.dx")

        # step to define binding site
        cmd = f"gistpp -i {gO_file} -i2 {lig} -op defbp -opt const {vol} -o {bp_out}"
        run_cmd(cmd)

        '''
        multiply each property by binding site (e.g. Etot.dx * bp_3.0.dx)
            and sum all the values in the region
        '''
        def do_mult(pref, datafile):
            out_file = f"bp{vol}_{pref}.dx"
            run_cmd(f"gistpp -i {bp_out} -i2 {datafile} -op mult -o {out_file}")
            return run_sum(out_file)

        result = {pref: do_mult(pref, path) for pref, path in data_paths.items()}
        results[vol] = result

    # save as csv
    df = pd.DataFrame(results).T
    csv_name = f"{target}_{structure}_{blck}_gistpp.csv"
    df.to_csv(os.path.join(inpath, csv_name))

    return f"{target}_{structure}_{blck} completed"




### Main Function ###
def main():
    # task list for parallel execution
    tasks = [(t, s, b, volumes, base_path)
             for t in targets
             for s in structures
             for b in blocks]

    total = len(tasks)
    print(f"Starting {total} combinations using {N_CPU} CPU cores...")

    # parallel running
    with ProcessPoolExecutor(max_workers=N_CPU) as executor:
        futures = [executor.submit(run_gist_combination, *task) for task in tasks]

        # process results
        for i, f in enumerate(as_completed(futures), 1):
            try:
                print(f"[{i}/{total}] {f.result()}")
            except Exception as e:
                print(f"Error: {e}")

    print("All tasks finished!")




if __name__ == "__main__":
    main()
    print(f"Total runtime: {time.time() - start:.2f} seconds")
