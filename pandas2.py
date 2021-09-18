import os, glob, sys
import pandas as pd
import numpy as np
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
cwd = (str(sys.argv[0][:-11]))
print(cwd)
path_current = Path(cwd)
# Assigns the current working directory 
# The path command allows for the retrieval of the parent directory
def codon_assignment():
    # Assigns all the codons which can code for amino acids 
    PHE = ["PHE", 'TTT', 'TTC']
    LEU = ["LEU", "TTA", "TTG", "CTT", "CTC", "CTA", "CTG"]
    ILE = ["ILE", "ATT", "ATC", "ATA"]
    MET = ["MET", "ATG"]
    VAL = ["VAL", "GTT", "GTC", "GTA", "GTG"]
    SER = ["SER", "TCT", "TCC", "TCA", "TCG", "AGT", "AGC"]
    PRO = ["PRO", "CCT", "CCC", "CCA", "CCG"]
    THR = ["THR", "ACT", "ACC", "ACA", "ACG"]
    ALA = ["ALA", "GCT", "GCC", "GCA", "GCG"]
    TYR = ["TYR", "TAT", "TAC"]
    HIS = ["HIS", "CAT", "CAC"]
    GLN = ["GLN", "CAA", "CAG"]
    ASN = ["ASN", "AAT", "AAC"]
    LYS = ["LYS", "AAA", "AAG"]
    ASP = ["ASP", "GAT", "GAC"]
    GLU = ["GLU", "GAA", "GAG"]
    CYS = ["CYS", "TGT", "TGC"]
    TRP = ["TRP", "TGG"]
    ARG = ["ARG", "CGT", "CGC", "CGA", "CGG", "AGG", "AGA"]
    GLY = ["GLY", "GGT", "GGC", "GGA", "GGG"]
    # Full list of all possible AAs with the first item in the list being the amino acid name
    AA = [PHE,LEU,ILE,MET,VAL,SER,PRO,THR,ALA,TYR,HIS,GLN,ASN,LYS,ASP,GLU,CYS,TRP,ARG,GLY]
    # Creates a list of lists using the amino acids 
    path = str(path_current.parent) + '/input'
    std_protein = str(protein) + '.'
    # Searches for the protein plus the "." character to ensure the correct protein is read
    # Ie if searching for "SEC4" searching for "SEC4" alone may incorrectly identify "SEC43" but searching for "SEC4." will not
    for codon_file in glob.glob(os.path.join(path, '*.txt')):
        with open(os.path.join(os.getcwd(), codon_file), 'r') as current_codon_file:
            mylist = [line.rstrip('\n') for line in current_codon_file]
            # See commnets in input_file.py for an explanation of how the search works
            for file_line in mylist:
                # Searches for protein in codon file
                if std_protein in file_line:
                    place = mylist.index(file_line)
                    # Retrieves the line number containing the protein
                    place = place + 1
                    # Reads the next line to find the codon sequence
                    file_line = mylist[place]
                    codons_sequence = file_line
                    # codons_sequence provides a length for the next command
    n = 3 
    chunks = [codons_sequence[i:i+n] for i in range(0, len(codons_sequence), n)]
    # Splits the line containing the codon sequence into chunks of 3 codons each
    for codon in chunks:
        for sublist in AA:
            if codon in sublist:
                # Assigns an AA per codon chunk
                with open(str(path_current.parent) + '/script_content/codons/codon2.txt', 'a') as AA_print_out:
                    # Prints out AA sequence from gb file to a second file 
                    with redirect_stdout(AA_print_out):
                        print(sublist[0])
                        # Prints out the first entry in the list which is the amino acid name ie "ARG"

file = open(str(path_current.parent) + "/script_content/Protein_name/name.txt")
# Reads the protein name
line = file.read().replace("\n", "")
# removes \n from name.txt for later use
file.close()
protein = str(line)
# assigns value for proetin from name.txt (see script.py)

df = pd.read_csv(str(path_current.parent) + '/script_content/sasa/name.defattr', sep="\t", header=None, skiprows=3)
# Reads the name attribute file created by the script which contains the amino acid sequence 
df.columns = ['Blank', 'Residue', 'Name']
del df['Blank']
# Removes a blank column which is a relic from ChimeraX (empty column included in ChimeraX file)
df['Residue'] = df['Residue'].str[3:]
#   Converts the residue column (orgionally in the format of "/A:159" into an integer "159")
Exposure = pd.read_csv(str(path_current.parent) + '/script_content/csvs/attrcalc.csv', header=None, skiprows=1)
Exposure.columns = ['Residue', 'Exposure']
del Exposure['Residue']
# Extracts just the exposure values as the residues have already been imported from name.defattr

path = str(path_current.parent) + '/script_content/residues_trp'
for TRP_clashes in glob.glob(os.path.join(path, '*.defattr')):
    #   Searches for clash files output by script
    with open(os.path.join(os.getcwd(), TRP_clashes), 'r') as current_TRP_clash:
       #    Opens file in read only mode
        for x, line in enumerate(current_TRP_clash):
            if x == 6:
                # reads line 6 from each file (contains number of clashes) 
                with open(str(path_current.parent) + '/script_content/Clashes/TRP.txt', 'a') as TRP_text:
                    with redirect_stdout(TRP_text):
                        print(line, end='\n')
                        # prints out a text file containing only the number of clashes
TRP_clash_file = pd.read_csv(str(path_current.parent) + '/script_content/Clashes/TRP.txt', header=None)
TRP_clash_file[0] = TRP_clash_file[0].str.replace(r'clashes', '')
# deletes the word clashes to just export the integer value

# Repeats for ARG data: 
path = str(path_current.parent) + '/script_content/residues_arg'
for ARG_clashes in glob.glob(os.path.join(path, '*.defattr')):
    with open(os.path.join(os.getcwd(), ARG_clashes), 'r') as current_ARG_clash:
        for x, line in enumerate(current_ARG_clash):
            if x == 6:
                with open(str(path_current.parent) + '/script_content/Clashes/ARG.txt', 'a') as ARG_text:
                    with redirect_stdout(ARG_text):
                        print(line, end='\n')
ARG_clash_file = pd.read_csv(str(path_current.parent) + '/script_content/Clashes/ARG.txt', header=None)
ARG_clash_file[0] = ARG_clash_file[0].str.replace(r'clashes', '')

# Combines all values previously into one dataframe
df.insert(2, "Exposure", Exposure)
df.insert(2, "TRP", TRP_clash_file)
df.insert(2, "ARG", ARG_clash_file)
# Exports final dataframe into a single .csv file contained in raw_data
path_parent = path_current.parent
path_parent_2 = path_parent.parent
print(df)
df.to_csv(str(path_parent_2) + '/best_residues/raw_data/' + str(protein) + '.csv', index=False)

try:
    codon_assignment()
except Exception as Argument:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(str(path_parent_2) + '/error_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "Error encountered while producing output file with protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
    # Writes into the error log any errors encountered
    f.close()
try:
    df = pd.read_csv(str(path_current.parent) + '/script_content/codons/codon2.txt', header=None)
    # Reads the codon file created by codon_assignment
    df.index += 1 
    df['Residue'] = df.index
    # assigns the residue column as the index so the amino acid sequence from the .fna and .pdb files can be alligned
    df['Residue']=df['Residue'].astype(int)
    df2 = pd.read_csv(str(path_parent_2) + '/best_residues/raw_data/' + str(protein) + '.csv')
    df2 = df2.dropna()
    # drops any missing values
    df2 = pd.merge(df, df2)
    # merges the two data frames
    # df is the codon sequence from the .fna file and df2 is the raw data file
    df2.columns = ['Test', 'Residue', 'Name', 'ARG', 'TRP', 'Exposure']
    # Assigns the column names for the merged dataframe
    comparison_column = np.where(df2['Test'] == df2['Name'], True, False)
    df2['Sanity_check']= comparison_column
    total_lentgth = len(df2)
    # Tests is the sequence from the .fna file and the .pdb file match and assigns this column as "Sanity_check"
    indexFALSE = df2[df2['Sanity_check'] == False].index
    #df2.drop(indexFALSE, inplace=True)
    true_length = len(df2)
    if true_length < 0.5 * total_lentgth:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f = open(str(path_parent_2) + '/error_log.txt', "a")
        f.write("\n" + str(dt_string) + "\n" + "PDB match against fna file failed with protein: " + str(protein) + "\nPlease manually review" "\n")
        # Records the time analysis begins and the identity of the protein being analysed
        f.close()
        df2["Sanity_check"].replace({True: "ERROR", False: "ERROR"}, inplace=True)
except:
    df2 = pd.read_csv(str(path_parent_2) + '/best_residues/raw_data/' + str(protein) + '.csv')
    df2 = df2.dropna()
    df2["Sanity_check"] = "Missing data"
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(str(path_parent_2) + '/error_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "No fna file found. Unable to confirm protein identity\n")

sum_column = df2["ARG"] + df2["TRP"]
sum_of_clashes = sum_column
df2.insert(4, "clash sum", sum_of_clashes)
df2.to_csv(str(path_parent_2) + '/best_residues/raw_data/' + str(protein) + '.csv', index=False)
# Produces a sum of the number of clashes with TRP and ARG for each residue
indexMET = df2[df2['Residue'] == 1].index
df2.drop(indexMET, inplace=True)
# Drops any residue which contains a value for the residue column as "1" ie the first residue
# Inserts this sum as a new column
df2 = df2.sort_values(["clash sum", "Exposure"], ascending = (True, False))
# Sorts values firstly by number of clashes (0 clashes top) then by exposure (most exposed top)
indexclash = df2[ df2['clash sum'] > 3 ].index
df2.drop(indexclash , inplace=True)
# Drops any residue which contains a total number of clashes greater than 3
indexexposure = df2[ df2['Exposure'] < 20 ].index
df2.drop(indexexposure , inplace=True)
df = pd.read_csv(str(path_current.parent) + '/script_content/codons/codon2.txt', header=None)
length = len(df)
length = length - 20
indexlength = df2[df2['Residue'] > length].index
df2.drop(indexlength, inplace=True)
# Drops any residue which contains an exposure less than 20
indexFALSE = df2[df2['Sanity_check'] == False].index
df2.drop(indexFALSE, inplace=True)
#indexFALSE = df2[~(df2['Sanity_check'] == 'TRUE')].index
# Drops any residue which does not match with the .fna sequence
# orders the data
print(df2)
df2.to_csv(str(path_parent_2) + '/best_residues/modified_data/' + str(protein) + '.csv', index=False)
# prints out a .csv in the "modified_data" folder
# This final csv will contain the best residues most likley to tolerate substitution in order from best to worst
# All residues featured in this file will be confirmed against the .fna file and will be deemed to be tolerant to substitution
