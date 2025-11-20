# AI_Structure_Solvation

## GIST Post-Processing (GISTPP) Integration Pipeline

### Integration Workflow
The integration process follows these steps:
1. `gistpp_fcn.py` → 2. `integration_fcn.py` → 3. `process_gistpp_results.py`

**Step descriptions:**
* **gistpp_fcn.py**: Preprocessing step to prepare GIST results for integration
* **integration_fcn.py**: Iterates through all combinations (targets × structures × blocks × volumes) to integrate energy and hydrogen bond properties
* **process_gistpp_results.py**: Post-processes integrated results and generates final reports

---

## Non-Integration Scripts

* **FindCentroid.py**: Calculates the centroid of protein/ligand structures required for GIST runs
* **extract_ligand.py**: Extracts ligand structures needed for GIST results integration (binding site selection). Check usage with `python extract_ligand.py -h`
* **make_avg_submit_file.py**: Generates cpptraj input files for computing time-averaged structures from trajectories
* **gen_tleap.py**: Generates tLeap input files for system prep. Check usage with `python gen_tleap.py -h`
