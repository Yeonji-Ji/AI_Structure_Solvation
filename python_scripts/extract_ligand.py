from pymol import cmd
import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required arguments')

requiredNamed.add_argument("--pdb", dest='pdb', help="input file, expected to be in .pdb format", type=str, required=True)
requiredNamed.add_argument("--avg", dest="avg", help="input file, expected to be in .pdb format", type=str, required=True)
requiredNamed.add_argument("--ligand", dest='ligand', help="ligand molecule residue name", type=str, required=True)

parser.add_argument("--top", dest='top', help="(Optional) input file, expected to be in .prmtop format", type=str, required=False)
parser.add_argument("--crd", dest='crd', help="(Optional) input file, expected to be in .rst7 format", type=str, required=False)
parser.add_argument("--pref", dest='prefix', help="(Optional) boolean to set the dimensions to even by default", type=str, default=False)
args = parser.parse_args()

pdb = args.pdb
ligand = args.ligand
average = args.avg

cmd.load(pdb, "pdb")
if args.top and args.crd:
    cmd.load(args.top, "struct")
    cmd.load(args.crd, "struct")
else:
    cmd.load(average, "struct")

cmd.align("pdb", "struct")
cmd.select("lig", "pdb and resname " + ligand)
if args.prefix:
    pref = args.prefix
    cmd.save(f"{pref}.pdb", "lig")
else:
    cmd.save("ligand.pdb", "lig")
