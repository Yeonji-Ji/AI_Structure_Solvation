import argparse
import os

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required arguments')

requiredNamed.add_argument("--path", dest="path", help="directory to save files", type=str, required=True)
requiredNamed.add_argument("--target", dest='target', help="target name", type=str, required=True)
parser.add_argument("--af_n", dest="af_n", help="number of alphafold structures", type=int, required=False)
parser.add_argument("--bz_n", dest="bz_n", help="number of boltz structures", type=int, required=False)

args = parser.parse_args()

path = args.path
target = args.target

struct = ["xtal"]
if args.af_n:
    for i in range(args.af_n):
        st = f"af_{str(i)}"
        struct.append(st)
if args.bz_n:
    for i in range(args.bz_n):
        st = f"bz_{str(i)}"
        struct.append(st)

for st in struct:
    os.chdir(path)
    os.chdir(f"{target}_{st}")
    leap_name = f"tleap_{st}.in"
    pdb = f"{target}_{st}_4amb.pdb"
    prmtop = f"{target}_{st}.prmtop"
    rst7 = f"{target}_{st}.rst7"
    with open(leap_name, "w") as f:
        f.write("source leaprc.protein.ff19SB\n")
        f.write("source leaprc.water.opc\n")
        f.write(f"p=loadpdb {pdb}\n")
        f.write("check p\n")
        f.write("solvatebox p OPCBOX 10\n")
        f.write(f"saveamberparm p {prmtop} {rst7}\n")
        f.write("quit")
