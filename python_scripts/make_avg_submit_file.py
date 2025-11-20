import os

targets = ["wee1"]
structures = ["xtal", "af_0", "af_1", "af_2", "af_3", "af_4"]
avg_range = [1, 100000, 10]    # [start_frame, end_frame, offset]

# base directory
base_path = f"/gibbs/yeonji/34_DUDE"
# submit directory
submit_path = f"/water/home/yeonji/34_DUDE"

for target in targets:
    for structure in structures:
        inpath = f"{base_path}/{target.upper()}/{structure}"
        outpath = f"{submit_path}/{target.upper()}/{structure}"

        # Change the file name
        top = f"{target}_{structure}.prmtop"
        traj = "md10.nc"

        avg = f"{target}_{structure}_avg.pdb"
        cpptraj_input_file = f"{outpath}/{structure}_avg_cpptraj.in"

        parm = f"parm {inpath}/{top}\n"
        trajin = f"trajin {inpath}/{traj} {str(avg_range[0])} {str(avg_range[1])} {str(avg_range[2])}\n"
        average = f"average {inpath}/{avg} pdb (!:WAT)\n"
        run = "run\n"
        quit = "quit"

        with open(cpptraj_input_file, "w+") as f:
            f.write(parm + trajin + average + run + quit)
            f.close()
