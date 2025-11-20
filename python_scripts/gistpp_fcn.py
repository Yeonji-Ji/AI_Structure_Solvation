from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess
import os
import time

############################################################
# GISTPP Calculation (target × structure × block × volume) #
############################################################

targets = ["wee1"]
blocks = ["80_100"]
structures = ["xtal"]
# base directory
base_path = f"/gibbs/yeonji/34_DUDE/"

### Run command function ###
def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

### Run the first step of gistpp
def process_gistpp(target, structure, block):
    """Runs all gistpp steps for one combination."""
    inpath = f"{base_path}/{target.upper()}/{structure}/gist/{block}"
    outpath = f"{base_path}/{target.upper()}/{structure}/gistpp/{block}"
    os.makedirs(outpath, exist_ok=True)

    read = {
        "gO": f"{inpath}/Gist4-gO.dx",
        "Esw_dens": f"{inpath}/Gist4-Esw-dens.dx",
        "Eww_dens": f"{inpath}/Gist4-Eww-dens.dx",
    }

    out = {
        "grho": f"{outpath}/grho.dx",
        "Esw": f"{outpath}/Gist4-Esw.dx",
        "Eww": f"{outpath}/Gist4-Eww.dx",
        "Etot": f"{outpath}/Gist4-Etot.dx",
        "sasa": f"{outpath}/sasa_o.dx",
    }

    voxel = 0.125
    const1 = voxel * 0.0333
    const2 = voxel * 0.5

    run(f"gistpp -i {read['gO']} -op multconst -opt const {const1} -o {out['grho']}")
    run(f"gistpp -i {read['Esw_dens']} -op multconst -opt const {const2} -o {out['Esw']}")
    run(f"gistpp -i {read['Eww_dens']} -op multconst -opt const {voxel} -o {out['Eww']}")
    run(f"gistpp -i {out['Esw']} -i2 {out['Eww']} -op add -o {out['Etot']}")
    run(f"gistpp -i {out['grho']} -op sasa -o {out['sasa']}")
    run(f"rm {outpath}/*dens.dx")

    return f"{target}_{structure}_{block} done"


if __name__ == "__main__":
    start = time.time()
    tasks = [(t, s, b) for t in targets for s in structures for b in blocks]

    with ProcessPoolExecutor() as ex:
        futures = [ex.submit(process_gistpp, *task) for task in tasks]
        for i, f in enumerate(as_completed(futures), 1):
            print(f"[{i}/{len(futures)}] {f.result()}")

    print(f"Total runtime: {time.time() - start:.2f} sec")
