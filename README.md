# List of scripts

I expect these scripts to be run in gpvms

## Scripts for starting SL7 container

I include scripts for sbnd.
```
open_SL7_sbnd.sh
```
- Opens an SL7 container

```
setup_SL7_sbnd.sh
```
- Source `setup_sbnd.sh` and setup `sbndcode`. For now, I am using `sbndcode v10_04_06_01`. But it should be updated in future.

## Script for making file lists in xrootd format

Scripts require SL7 container and samweb.

```
filelisting_with_samweb_def.py
```
- Creats list of files using samweb query or definition as input
- Modify `this_query`, `experiment` and `output_file_name` to run


```
filelisting_with_dir.py
```
- Creats list of root file in a directory.
- Modify `Sample`. First element is for output list file name and second element is for the input directory.

```
make_flatcaf_filelist.py
make_largest_root_filelist.py
```
- These scripts are for making file list of a direcoty that eash root files is inside in each direcoty (like output of project.py).
- The `make_flatcaf_filelist.py` is for collecting flatcaf files in the case that multiple root files like caf, flatcaf.caf are in a directory.
- The `make_largest_root_filelist.py` is for collecting the largest root file in size for each sub-directory. It is useful sometimes.


## Scripts for submitting grid jobs for merging files: hadd root files

Thses scrips are from Jeasung Kim (jedori0228).

```
makeScripts.py
```

- A main script for grib job submission.
- Modify 'tier' that is used for output root file names.
- Modify `Samples`. First element is for xrootd file list as input and second element is for output directory.
- Modify `NTarget`. This is number of root files that after merging root files in the input xrootd file list defined in `Samples`.


```
grid_executable.sh
```

- A script run in each grid node.
- Modify `export TIER` line to agree with `tier` in `makeScripts.py`. Otherwise, hadd'ed root file will not be transferred to the output directory.