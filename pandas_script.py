import pandas as pd
import sys
from pathlib import Path
cwd = (str(sys.argv[0][:-17]))
path_current = Path(cwd)
# assigns cwd see script.py  
attrcalc = pd.read_csv(str(path_current.parent) + '/script_content/sasa/sasa.defattr', sep = "\t", header = None, skiprows = 3)
#   Reads the output file from CHimeraX, first three rows are details from ChimeraX so are skipped, lines seperated using /t
attrcalc.columns = ['Blank', 'Residue', 'exposure']
del attrcalc['Blank']
#   Relic from the import of the output file (empty column included in ChimeraX file)
attrcalc.to_csv(str(path_current.parent) + '/script_content/csvs/attrcalc.csv', index=False)
# Exports this file a csv 
exposure_residues = pd.read_csv(str(path_current.parent) + '/script_content/csvs/attrcalc.csv')
residues= exposure_residues["Residue"]
#   Creates a new pandas dataframe using the residue column
df= residues
#   Assigns this as the active dataframe
df.to_csv(str(path_current.parent) + '/script_content/csvs/Residues.csv', index=False, header=None)
#   Exports a file containing just the residue infromation 
