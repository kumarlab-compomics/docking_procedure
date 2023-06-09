# Requirements
* AutoDock Tools script and pythonsh from MGL
* `.bashrc` with relevant aliases for molecule prep scripts like `prepare_ligand4.py`:

```bash
export PATH=~/mgltools_x86_64Linux2_1.5.7/bin:$PATH #

alias pmv='~/mgltools_x86_64Linux2_1.5.7/bin/pmv'           # not neccessary
alias adt='~/mgltools_x86_64Linux2_1.5.7/bin/adt'           # not neccessary
alias vision='~/mgltools_x86_64Linux2_1.5.7/bin/vision'     # not neccessary
alias pythonsh='~/mgltools_x86_64Linux2_1.5.7/bin/pythonsh' # important

alias prep_prot='pythonsh ~/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py'   # important
alias prep_lig='pythonsh ~/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py'      # important
```
# AutoDock Vina Procedure

## 1. Install AutoDock Vina
Can install using wget and unzip in Linux (see https://vina.scripps.edu/downloads/ for other OS):
```bash
wget https://vina.scripps.edu/wp-content/uploads/sites/55/2020/12/autodock_vina_1_1_2_linux_x86.tgz
```
```bash
tar -xvzf autodock_vina_1_1_2_linux_x86.tgz
```
Directory should match the following
```bash
autodock_vina_1_1_2_linux_x86/LICENSE
autodock_vina_1_1_2_linux_x86/bin/
autodock_vina_1_1_2_linux_x86/bin/vina
autodock_vina_1_1_2_linux_x86/bin/vina_split
```

Run the following to test if it works:
```bash
./autodock_vina_1_1_2_linux_x86/bin/vina --help
```
***
## 2. Installing AutoDock Tools (ADT)

For preparing the receptor and ligand we will use AutoDock Tools (ADT) from MGL. ADT is a GUI for preparing the receptor and ligand, however it comes with python scripts that we can run from the cmd line. Also it includes a prebuilt Python 2.0 interpreter called `pythonsh` that we can use to run the scripts.

Download ADT from http://mgltools.scripps.edu/downloads/ and unzip. 
```bash
wget https://ccsb.scripps.edu/mgltools/download/491/mgltools_x86_64Linux2_1.5.7p1.tar.gz
```
```bash
tar -xvzf mgltools_x86_64Linux2_1.5.7p1.tar.gz
```
Run install script
```bash
cd mgltools_x86_64Linux2_1.5.7 ; ./install.sh
```
>NOTE if you get the following error:
>```bash
>./install.sh: 79: export: (x86)/Common: bad variable name
>```
>This is because mgl automatically trys to add the `bin` directory to the root,, just uncomment that line (line 79) and you should be good.

Now we have `pythonsh` and ADT installed, they should be located in:
```bash
mgltools_x86_64Linux2_1.5.7/bin/pythonsh

mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py
mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py
```

>We also have `prepare_flexreceptor4.py` which can be used to prepare a receptor with flexible side chains. However, this is not used in this tutorial.

To test if ADT is working add `pythonsh` to your `.bashrc` as an alias and run the following:
```bash
pythonsh mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py --help
```
***
## 3. Preparing receptor and ligand PDBQT files
The receptor must be cleaned of water molecules and other non-residue molecules. The receptor must also be converted to a pdbqt file that includes charge (Q) and atom type (T) information. This can be done using the `prepare_receptor4.py` script from ADT.

There are two ways to prepare the receptor depending on the PDB file you have:

### *3.2.A Receptor + ligand as PDB complex*
> For PDBbind we can download structures using wget as with `wget http://www.pdbbind.org.cn/v2007/10gs/10gs_complex.pdb` where `10gs` is the PDB ID

If the receptor and ligand already exist as a complex in a single PDB file, then run `prep_pdb.sh` with the following arguments. It will clean the file and split it into ligand and receptor pqbqt files.
```bash
prep_pdb.sh <path> <pdbcode> <ADT_path>
```
>To get help message run `prep_pdb.sh` with no arguments.

The `<path>` directory should now contain the following files:
```bash
<pdbcode>.pdb
prep/<pdbcode>-split-<num_atoms>_ligand.pdbqt
prep/<pdbcode>-split-<num_atoms>_receptor.pdbqt
```

### *3.2.B Receptor on its own*
If the receptor is on its own in a PDB file, then run `prep_receptor.sh` with the following arguments. It will clean the file and convert it to a pdbqt file.
```bash
prep_receptor.sh <path> <pdbcode> l <ADT_path>
```

Then for the ligand you need to download its SDF file and prepare it using OpenBabel or similar tools... 
>***TODO***

### **3.3 Preparing Grid files**
For AutoDock Vina grid files and AutoGrid are not needed (see "AutoDock Tools Compatibility": https://vina.scripps.edu/manual/).

From Vina help message we can see how to input the search space:
```bash
Input:
  --receptor arg        rigid part of the receptor (PDBQT)
  --flex arg            flexible side chains, if any (PDBQT)
  --ligand arg          ligand (PDBQT)

Search space (required):
  --center_x arg        X coordinate of the center
  --center_y arg        Y coordinate of the center
  --center_z arg        Z coordinate of the center
  --size_x arg          size in the X dimension (Angstroms)
  --size_y arg          size in the Y dimension (Angstroms)
  --size_z arg          size in the Z dimension (Angstroms)

Output (optional):
  --out arg             output models (PDBQT), the default is chosen based on 
                        the ligand file name
  --log arg             optionally, write log file

Misc (optional):
  --cpu arg                 the number of CPUs to use (the default is to try to
                            detect the number of CPUs or, failing that, use 1)
  --seed arg                explicit random seed
  --exhaustiveness arg (=8) exhaustiveness of the global search (roughly 
                            proportional to time): 1+
  --num_modes arg (=9)      maximum number of binding modes to generate
  --energy_range arg (=3)   maximum energy difference between the best binding 
                            mode and the worst one displayed (kcal/mol)

Configuration file (optional):
  --config arg          the above options can be put here

Information (optional):
  --help                display usage summary
  --help_advanced       display usage summary with advanced options
  --version             display program version
```

This search space should be centered at the binding pocket and can be retrieved from the PDB file if provided as a complex. The size of the search space should be large enough to cover the entire binding pocket.

To create a config file with the search space provided, run the following:
```bash
python prep_conf.py -r <prep_path>
```
***
## 4. Running AutoDock Vina

Now that we have the prepared receptor, ligand, and `conf.txt` file set up, we can run AutoDock Vina.

To do so run the following:
```bash
vina --config <path>conf.txt
```

# Errors
In the `test` directory there are some files that can be used to test if everything is working correctly. They are what comes out of the `prep_pdb.sh` script. To make sure that you have set up everything correctly, you can run the following to test and compare the results to the `test` directory:
```bash
prep_pdb.sh ./test 1a1e <PATH>/mgltools_x86_64Linux2_1.5.7/MGLToolsPckgs/AutoDockTools/Utilities24/
```
Make sure to replace `<PATH>` with the path to your mgltools directory.
