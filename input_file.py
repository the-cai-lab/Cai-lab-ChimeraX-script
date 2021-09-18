import csv, os, csv, glob, sys
from itertools import islice
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
cwd = (str(sys.argv[0][:-14]))
path_current = Path(cwd)
path_parent = path_current.parent
path_parent_2 = path_parent.parent

def codon_file_builder():
    with open(str(path_parent_2) + '/Protein list.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        # Reads through the protein list provided by the user
        for row in reader:
            for std_protein in row:
                protein1 = '' + str(std_protein) + ']'
                # Adds the character ']' to ensure that the correct proteins are read in the .fna file
                # .fna files use the format "[gene=TDA8]" so by using the ']' character this ensures that only the correct protein is read
                print("Reading codon sequence for proetin: " + std_protein)
                # Prints out the above statement in the command line informing the user which protein is being analysed
                path = str(path_parent_2) + '/pdb'
                for fna_file in glob.glob(os.path.join(path, '*.fna')):
                    # searches for .fna file provided by the user
                    with open(os.path.join(os.getcwd(), fna_file), 'r') as current_file:
                        mylist = [line.rstrip('\n') for line in current_file]
                        # Converts file into a list
                        mol_place = 0
                        place = 0
                        for file_line in mylist:
                            if protein1 in file_line:
                                # Searches for protein within the list created
                                place = mylist.index(file_line)
                                # Records the line number where the protein was found
                                place = place + 1
                                # Records the next line
                                start_line = place
                                with open(str(path_parent) + '/input/codon.txt', 'a') as codon_file:
                                    with redirect_stdout(codon_file):
                                        print("")
                                        print(std_protein + ".")
                                        # Prints out the protein being analysed into a text file 
                                        # The character "." is used so that later scripts can select for the correct protein by searching for "protein" + "."
                                while mol_place != place:
                                    file_line = mylist[place]
                                    if file_line[0] == '>':
                                        # lines containing the codon sequence begin with a letter while lines containing protein information begin with ">"
                                        # By searching the the next line with ">" the script idnetifies all lines containing the codon sequence
                                        mol_place = mylist.index(file_line)
                                        end_line = mol_place
                                        for file_line in mylist[start_line:end_line]:
                                            with open(str(path_parent) + '/input/codon.txt', 'a') as codon_file:
                                                with redirect_stdout(codon_file):
                                                    # prints out the codon sequence
                                                    print(file_line, end="", flush=True)
                                                        # prints the whole sequence onto a single line making it simple to analyse by other scripts 
                                                        # This allows other scripts to search for "protein" + "." and then read the next line for the codon sequence
                                    else:
                                        place = place + 1


def Chain_finder():
    path = str(path_parent_2) + '/pdb'
    # This is another method to select for only the protein being analysed
    # The pdb file may list multiple names for the same protein
    # If the protein is the last name (or only name) in the line it will end with ";" if it is not the last protein it will end with ","
    # Searching for these extra characters prevents errors ie searching for "SEC4" may incorrectly select "SEC43" while searching for "SEC4," will not
    print("Finding protein: " + std_protein + "in pdb file")
    # Prints out the above statement in the command line informing the user which protein is being analysed
    path = str(path_parent_2) + '/pdb'
    for pdb_file in glob.glob(os.path.join(path, '*.pdb')):
        with open(os.path.join(os.getcwd(), pdb_file), 'r') as current_pdb_file:
            head = list(islice(current_pdb_file, 500))
            # Looks in the first 500 lines of the pdb file
            # pdb files can contain over 100,000 lines so it is a waste to analyse all lines
            # All pdb files analysed to date have featured the protein before line 500 should a pdb file feature it after line 500 this will result in an error and this value should be changed
            mylist = [line.rstrip('\n') for line in head]
            mol_place = 0
            place = 0
            start_line = 0
            skip = "TITLE"
            for file_line in mylist:
                for match in matches:
                    if match in file_line:
                        place = mylist.index(file_line)
                        if skip in file_line:
                            place = place + 1
                        else:
                            place = place - 1
                        # Similar searching method as featured above
                        # In this case the previous lines rather than the following lines must be searched for the line MOL_ID
                            while mol_place != place:
                                file_line = mylist[place]
                                if 'MOL_ID:' in file_line:
                                    mol_place = mylist.index(file_line)
                                else:
                                    place = place - 1
                            mol_id = mylist[mol_place][11:].strip('SOURCE').strip('MOL_ID:')
                            mol_id = "MOL_ID:" + str(mol_id)
                            mol_place = mol_place + 1
                            print(mol_place)
                            for file_line in mylist[0:mol_place]:
                                if mol_id in file_line:
                                    print(mol_id)
                                    start_line = mylist.index(file_line)
                                    # Once the line MOLD_ID has been found the script will take this line and search for the realted chain associated with the MOL_ID
                                    for file_line in mylist[start_line:100]:
                                        if 'CHAIN:' in file_line:
                                            chain_list1 = file_line[17:].strip().strip(';').split(', ')
                                            chain_list.append(chain_list1)
                                            print(chain_list)
                                                # Once the chain has been identified takes the line and removes the first characters along with ";" and seperates values using ","
                                            mylist = [line.rstrip('\n') for line in head]
                                            for file_line in mylist:
                                                if file_line[0:6] == 'HEADER':
                                                    PDB_name1 = file_line[61:].strip()
                                                    print(PDB_name1)
                                                    PDB_name.append(PDB_name1)
                                                    print(PDB_name)
                                                    # Searches for the PDB name (first line) and records the PDB name featured here
                                                    print("Match found for protein: " + std_protein + " in pdb file: " + PDB_name1)
                                                    # Prints a message for the user in the command line informing them that the protein has been found
                                            break
    return chain_list[0], PDB_name[0]


    # Records the first chain found 
    # (only the first chain will be analysed so if protein on chains A,B,C only chain A will be analysed)
    # Records the Protein data bank name associated with the protein
failed_proteins = []
try:
    codon_file_builder()
except Exception as Argument:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(str(path_parent_2) + '/error_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "Error encountered while reading .fna file to build codon file\n" +
            "Error: " + str(Argument) + "\n")
    # Records the error along with the time this error occurred
    f.close()
    pass

path = str(path_parent_2) + '/pdb'
with open(str(path_parent_2) + '/Protein list.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        for std_protein in row:
            chain_list = []
            PDB_name = []
            try:
                matches = [std_protein + ",", std_protein + ";", std_protein + ")"]
                chains = Chain_finder()[0]
                # Assigns chains as the first value in chain finder (ie the chain)
                for chain in chains:
                    prot1 = '/' + str(chain)
                    prot1 = prot1.strip(',').strip(';')
                    # Adds on the character "/" to the chain ie "A" becomes "/A"
                    # This allows ChimeraX to use it as the chain variable
                PDB_name = Chain_finder()[1]
                # The Protein data bank name is also retrieved 
                with open(str(path_parent) + '/input/input.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([prot1, std_protein, PDB_name])
                    # Records a record in the input csv which will be read by the main script 
                    # Firstly the chain is recorded, next the standard protein name and finally the protein data bank file which contains the protein  
            except Exception as Argument:
                failed_proteins.append(std_protein)
                pass

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
f = open(str(path_parent_2) + '/error_log.txt', "a")
f.write("\n" + str(dt_string) + "\n" + "Unable to locate the following proteins: " + str(failed_proteins) + "\n")
f.close()
