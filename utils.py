# %%
from typing import List
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

def split_structure(file_path='sample_data/1a1e.pdbqt', save='all') -> List[str]:
    """
    Splits a pdbqt file if duplicate protein structures are present and saves the 
    largest structure to a new file under the same name postfixed by "-split.pdbqt".
    
        "TER" - determines the end of a protein structure as per the 
        pdb format.
        
    For more information on the pdb format see:
    http://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#TER
    
    args:
        file_path (str): path to pdbqt file (processed PDB file using 
        AutoDockTools - prepare_receptor4.py).
        save (str): save option depending on needs:
            'all', saves all structures to new files with additional postfix "-split-<length>.pdbqt".
            'mains', saves main protein and ligand (if present) to new files.
            'largest', saves largest structure to new file.
    
    returns:
        List[str]: list of structures present in the pdbqt file.
    """
    assert save in ['all', 'mains', 'largest'], f'Invalid save option: {save}'
    extens = file_path.split('.')[-1]
    print(extens)
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        structures = []
        i=0
        while i < len(lines):
            structure = []
            while lines[i][:3] != 'TER':
                structure.append(lines[i])
                i += 1
            structure.append(lines[i])
            structures.append(structure)
            i += 1
        
    # saving all structures to new files
    if save.lower() == 'all':
        saved_files = {}
        for structure in structures:
            # making sure no files are overwritten
            fp = f'{file_path.split(".")[0]}-split-{len(structure)}'
            postfix = f'-{len(structure)}_{saved_files.get(len(structure), 0)}.{extens}'
            
            with open(fp + postfix, 'w') as f:
                f.writelines(structure)
            saved_files[len(structure)] = saved_files.get(len(structure), 0) + 1
            
    elif save.lower() == 'mains':
        # saving main protein structure to new file
        lrgst=max(structures, key=len)
        fp = f'{file_path.split(".")[0]}-split-{len(lrgst)}.{extens}'
        with open(fp, 'w') as f:
            f.writelines(lrgst)
        print('wrote main file: ', fp)
            
        prot_df = get_df(lrgst)
        protein_center = prot_df[['x', 'y', 'z']].mean().values
        
        
        # saving closest structure to new file as the ligand
        if len(structures) > 1:
            # finding closest ligand structure to protein center
            lig_structure = None
            lig_dist = np.inf
            for structure in structures:
                if structure == lrgst: continue
                lig_df = get_df(structure)
                lig_center = lig_df[['x', 'y', 'z']].mean().values
                
                new_dist = np.linalg.norm(protein_center - lig_center)
                if new_dist < lig_dist:
                    lig_dist = new_dist
                    lig_structure = structure
                
            fp = f'{file_path.split(".")[0]}-split-{len(structure)}_ligand.{extens}'
            with open(fp, 'w') as f:
                f.writelines(lig_structure)

            print('wrote ligand file: ', fp)
                
        
    
    elif save.lower() == 'largest':
        # saving largest structure to new file
        fp = f'{file_path.split(".")[0]}-split-{len(structure)}.{extens}'
        with open(fp, 'w') as f:
            f.writelines(max(structures, key=len))
    
    return structures

def get_df(lines:List[str]) -> pd.DataFrame:
    """
    Returns a pandas DataFrame of pdb file.
    
    Columns (in order that they appear in the PDB format)
        'atom_name', 'count', 'atom_type', 'res_name', 'chain_name', 'res_num', 'x', 'y', 'z'
    
    Example of a line from PDB:
        ATOM      1  N   ILE A 146      57.904  24.527  16.458  *1.00  39.85     0.626 N
        everything after * is ignored.
    
    args:
        lines (List[str]): list of lines from pdb file.
    """
    cols = ['atom_name', 'count', 'atom_type', 
            'res_name', 'chain_name', 'res_num', 
            'x', 'y', 'z']
    strIO = StringIO(''.join(lines))
    df = pd.read_csv(strIO, sep=r'[ ]+', header=None, names=cols, 
                     usecols=cols, engine='python')
    df.dropna(inplace=True)
    return df

def get_ligand(file_path='sample_data/1a1e.pdbqt'):
    """
    Using proDy tool this will seperate the protein and ligand structures from the
    PDB file (before running prepare_receptor4.py).
    """
    pass

def plot_atoms(df, bounding_box=True):
    """plots atoms in 3D space using plotly"""
    fig = px.scatter_3d(df, x='x', y='y', z='z', color='res_num')
    
    # adding bounding box
    if bounding_box:
        max_x, max_y, max_z = df[['x', 'y', 'z']].max()
        min_x, min_y, min_z = df[['x', 'y', 'z']].min()
        
        # creating bounding box (8 corners/points)
        corners = [[min_x, min_y, min_z], [min_x, min_y, max_z], 
                   [min_x, max_y, max_z], [min_x, max_y, min_z], 
                   
                   [max_x, max_y, min_z], [max_x, max_y, max_z],
                   [max_x, min_y, max_z], [max_x, min_y, min_z],
                   
                   # connecting corners
                   [max_x, max_y, min_z], [max_x, max_y, max_z],
                   [min_x, max_y, max_z], [min_x, max_y, min_z],
                   [min_x, min_y, min_z], [max_x, min_y, min_z],
                   [max_x, min_y, max_z], [min_x, min_y, max_z]]
        
        fig.add_trace(go.Scatter3d(x=[c[0] for c in corners],
                                   y=[c[1] for c in corners],
                                   z=[c[2] for c in corners]))
        
    fig.show()

def plot_together(dfL,dfP):
    """plotting ligand and protein in 3D space"""
    fig = px.scatter_3d(dfP, x='x', y='y', z='z', color='res_num')
    fig.add_scatter3d(x=dfL['x'], y=dfL['y'], z=dfL['z'], line={"color":'#000000'}, 
                      marker={"color":'#000000'}, name='ligand')
    fig.show()


# %%
if __name__ == '__main__':
    # split_structure(file_path='sample_data/1a1e_n-e.pdb', save='mains')
    dfP = get_df(open('sample_data/1a1e_n-e-split-1031.pdbqt','r').readlines())
    dfL = get_df(open('sample_data/1a1e_n-e-split-41_ligand.pdbqt','r').readlines())
    
    plot_together(dfL,dfP)