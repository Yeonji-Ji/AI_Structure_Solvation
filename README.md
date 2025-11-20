# AI_Structure_Solvation

### Integration (GISTPP) steps:
gistpp_fcn.py -> integration_fcn.py -> process_gistpp_results.py

- gistpp_fcn.py:
The first step (preprocessing step) to integrate the GIST results.

- integration_fcn.py:
Loops to integrate energy & h-bonds properties for the combinations (target × structure × block × volume).

- process_gistpp_results.py:
Post-processing the results data to report. 


### Non integration scripts
- FindCentroid.py:
To find the centroid of the protein/ligand required for GIST run

- extract_ligand.py:
The ligand is required for GIST results integration (binding site selection). C
heck the usage with "python extract_ligand.py -h"

- make_avg_submit_file.py:
Generate the cpptraj input files for the time-average structure of the trajectory.

- gen_tleap.py:
Generates tLeap input files.
