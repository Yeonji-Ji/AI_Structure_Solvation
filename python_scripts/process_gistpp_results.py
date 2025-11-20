import pandas as pd
import numpy as np
import os

bulk_E = -12.259
targets = ["wee1"]
structures = ["xtal"]
blocks = ["80_100"]
volumes = [f"{v:.1f}" for v in np.arange(3.0, 10.5, 0.5)]
# base directory
base_path = f"/gibbs/yeonji/34_DUDE/"

columns = ["vol", "water", "dE", "dEsw", "dEww", "Nsw", "Nww", "E/water", "Esw/water", "Eww/water", "Nsw/water", "Nww/water"]

def process_result(target, structure, blck):
    inpath = f"{base_path}/{target.upper()}/{structure}/gistpp/{blck}"
    outpath = f"{base_path}/{target.upper()}/{structure}/gistpp/{blck}"

    gistpp = pd.read_csv(f"{inpath}/{target}_{structure}_{blck}_gistpp.csv", index_col=0)
    gistpp.reset_index(drop=True, inplace=True)

    out_file = f"{target}_{structure}_{blck}_int_3_10_result.csv"

    out_df = pd.DataFrame(columns=columns)

    out_df["vol"] = volumes
    out_df["water"] = gistpp["grho"].round(4)
    grho = gistpp["grho"].replace(0, np.nan)

    out_df["dE"] = (gistpp["Etot"] - (bulk_E * gistpp["grho"])).round(4)
    out_df["dEsw"] = gistpp["Esw"].round(4)
    out_df["dEww"] = (gistpp["Eww"] - (bulk_E * gistpp["grho"])).round(4)
    out_df["Nsw"] = (gistpp["Nsw_acc"] + gistpp["Nsw_don"]).round(4)
    out_df["Nww"] = (gistpp["Nww_acc"] + gistpp["Nww_don"]).round(4)
    out_df["E/water"] = (gistpp["Etot"] / grho).round(4)
    out_df["Esw/water"] = ((0.5 * gistpp["Esw"]) / grho).round(4)
    out_df["Eww/water"] = (gistpp["Eww"] / grho).round(4)
    out_df["Nsw/water"] = ((gistpp["Nsw_acc"] + gistpp["Nsw_don"]) / grho).round(4)
    out_df["Nww/water"] = ((gistpp["Nww_acc"] + gistpp["Nww_don"]) / grho).round(4)

    # print(out_df)

    # save the result
    os.makedirs(outpath, exist_ok=True)
    out_df.to_csv(os.path.join(outpath, out_file), index=False)

    return f"Saved: {out_file}"

for i, (target) in enumerate(targets, 1):
    for structure in structures:
        for blck in blocks:
            print(f"[{i}/{len(targets)}] Processing {target}_{structure}_{blck}")
            print(process_result(target, structure, blck))
