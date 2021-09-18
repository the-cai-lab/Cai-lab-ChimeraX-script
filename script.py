import chimerax, os, csv, sys, shutil, threading
from contextlib import redirect_stdout
from chimerax.core.commands import run
# If viewing from a text editor chimerax will appear as missing, so an error will be rasied 
# This script will only run within ChimeraX's own enviroment
from datetime import datetime
cwd = (str(sys.argv[0][:-10]))

# sys.argv is used to identify the current working directory as using __file__ is not an option in ChimeraX
# characters are removed from the end to leave cwd as the file location rather than the file itself

def print_name(): 
    with open( str(cwd) + '/script/script_content/Protein_name/name.txt', 'w') as protein_name:
        with redirect_stdout(protein_name):
            print(protein)

# prints a file with the protein name to make this variable acessible to external scripts

def clear_files():
    folder = str(cwd) + '/script/script_content'
    for files in os.listdir(folder):
        file_path = os.path.join(folder, files)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while clearing script files\n" + 'Failed to delete %s. Reason: %s' % (file_path, e) + "\n" + "Analysis aborted\n")
            f.close()

# Deletes any subfolders along with their contents from previous calculations. This also prevents the user introducing errors by altering the file structure.
# If this operation fails the script will terminate.

def create_files():
    path = str(cwd) + '/script/script_content'
    try:
        os.mkdir(str(path) + "/Clashes")
        os.mkdir(str(path) + "/csvs")
        os.mkdir(str(path) + "/Protein_name")
        os.mkdir(str(path) + "/residues_arg")
        os.mkdir(str(path) + "/residues_trp")
        os.mkdir(str(path) + "/sasa")
        os.mkdir(str(path) + "/codons")
    except OSError:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f = open(str(cwd) + '/error_log.txt', "a")
        f.write("\n" + str(dt_string) + "\n" + "Error encountered while creating script folders\n" + "Creation of the directory %s failed" % path + "\n" + "Analysis aborted\n")
        f.close()

# The required subfolders are rebuilt, if this operation fails the script will terminate. 

# The following 3 functions are input into ChimeraX 
# For details regarding any commands being used into ChimeraX please consult ChimeraX documentation 
# https://www.rbvi.ucsf.edu/chimerax/docs/user/index.html        
def sasa_function():
    run(session, "close all")
    # Closes any open ChimeraX sessions to prevent interference 
    run(session, "open " + str(PDB_name) + "")
    # Opens the pdb file being analysed (Please note this uses an online copy of the pdb file not the local copy so user edits will not interfer with the calculations)
    run(session, "sel "+ str(prot) + " & protein")
    # selectedOnly true ensures that only the chain being analysed is used for the name file (otherwise all chains will be printed to output files)
    run(session, "save " + str(cwd) + "/script/script_content/sasa/name.defattr attrName r:name format defattr selectedOnly true")
    # saves an attribute file containing the names of all residues (using only amino acid residues)
    run(session, "surface")
    #   Applies the surface command which produces a surface model of the molecule and area attributes
    run(session, "measure sasa " + str(prot) + " & protein setAttribute true")
    #   measures the solvent accessible surface area of each residue in the protein 
    run(session, "save " + str(cwd) + "/script/script_content/sasa/sasa.defattr attrName r:area format defattr matchMode any models " + str(prot) + " & protein")
    #   saves the surface area attribute calculated by the previous command

def clashes_function_TRP():
    #    Closes protein model (quickest method to use original protein data)
    run(session, "close all")
    run(session, "open " + str(PDB_name) + "")
    run(session, "swapaa " + str(residue) + " trp preserve 1 log false")
    # Swaps the AA in the first position with tryptophan using a rotamer as similar as possible to original protein
    run(session, "clashes " + str(residue) + " name clash1 setAttrs true attrName clash log false intraRes true overlapCutoff 0.4 saveFile " + str(cwd) + "/script/script_content/residues_trp/" + str(order).zfill(4) + str(residue_edited) + ".defattr")
    #    Records any clashes with nearby atoms using a cutoff of 0.4 Angstroms and then saves data into clash folder

def clashes_function_ARG():
    # Repeats for Argenine:
    run(session, "swapaa " + str(residue) + " arg preserve 1 log false")
    run(session, "clashes " + str(residue) + " name clash2 setAttrs true attrName clash log false intraRes true overlapCutoff 0.4 saveFile " + str(cwd) + "/script/script_content/residues_arg/" + str(order).zfill(4) + str(residue_edited) + ".defattr")
    run(session, "close all")
    run(session, "open " + str(PDB_name) + "")

def output():
    cmd = 'python ' + str(cwd) + '/script/subscripts/pandas2.py'
    os.system(cmd)
    # Runs pandas2.py in the OS

def start_running():
    cmd = 'python ' + str(cwd) + '/script/subscripts/script1.py'
    os.system(cmd)

def pandas():
    cmd = 'python ' + str(cwd) + '/script/subscripts/pandas_script.py'
    os.system(cmd)
    # Pandas_script is executed in the OS as ChimeraX cannot execute pandas scripts

def input():
    cmd = 'python ' + str(cwd) + '/script/subscripts/input_file.py'
    os.system(cmd)
# Runs the input file generator script in the OS

def clear_input_files():
    folder = str(cwd) + '/script/input'
    for files in os.listdir(folder):
        file_path = os.path.join(folder, files)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while clearing input files\n" + 'Failed to delete %s. Reason: %s' % (file_path, e) + "\n" + "Analysis aborted\n")
            f.close()

# Clears input files see clear_files (above) comments for details 

def running(): 
    with open(str(cwd) + '/running/running.txt', 'w') as running:
        with redirect_stdout(running):
            print("False")
# Tells the UI to start running using the running.txt file

def running_go():
    with open(str(cwd) + '/running/running.txt', 'w') as running:
        with redirect_stdout(running):
            print("Go")
# Prints the GO command for the UI (Causes the UI to stop printing "finding protein")

def clasherror():
    f = open(str(cwd) + "/script/script_content/residues_trp/" + str(order).zfill(4) + str(residue_edited) + ".defattr", "w")
    f.write("Allowed overlap: 0.4\nH-bond overlap reduction: 0.4\nIgnore clashes between atoms separated by 4 bonds or less\nDetect intra-residue clashes: True\nDetect intra-molecule clashes: True\n\n99 clashes\n")
    f.close
# For any residues which fail to be analysed will print out 99 clashes in their clash file

try:
    run(session, "close all")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # Records the date and time for the log
    f = open(str(cwd) + '/action_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "Starting analysis of pdb folder\n")
    # Writes into the action log that analysis is starting
    f.close()
    clear_input_files()
except Exception:
    sys.exit(1)
    # Aborts the operation if this function fails as the script cannot continue without the correct input files
try:
    running()
except Exception as Argument:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(str(cwd) + '/error_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "Error encountered while writing running file with protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
    f.close()
pass
try:
    clear_files()
except Exception:
    sys.exit(1)
    # Another fatal error which will result in terminiation of the script
try:
    create_files()
except Exception:
    sys.exit(1)
    # Another fatal error which will result in terminiation of the script

th = threading.Thread(target=start_running)
th.start()

try:
    input()
except Exception as Argument:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(str(cwd) + '/error_log.txt', "a")
    f.write("\n" + str(dt_string) + "\n" + "Error encountered while creating input file\n" + "Error: " + str(Argument) + "\n" + "Analysis aborted\n")
    # Writes into the error log any errors encountered 
    f.close()
with open(str(cwd) + '/script/input/input.csv', newline='') as Input_file:
    reader = csv.reader(Input_file)
    # Reads the input file created by the input script
    for row in reader:
        prot = row[0]
        # prot is the chain corresponding to the protein being analysed
        protein = row[1]
        # protein is the standard name of the protein
        PDB_name = row[2]
        # PDB_name is the name of the protein data bank file containing the protein 
        try:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/action_log.txt', "a")
            f.write(str(dt_string) + "\n" + "Starting analysis of protein: " + str(protein) + "\n")
            # Records the time analysis begins and the identity of the protein being analysed
            f.close()
        except Exception:
            pass
            
        try:
            print_name()
        except Exception as Argument:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while writing protein name with protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
            # Records an entry in the error log for any errors encountered during the analysis of each protein
            f.close()
            pass
        try:
            running_go()
        except Exception as Argument:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while writing running file with protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
            f.close()
        try:
            sasa_function()
        except Exception as Argument:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while calculating solvent surface area with protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
            f.close()
            pass
        try:
            pandas()
        except Exception as Argument:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while producing csvs for protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
            f.close()
            pass
        order = 0
        # Assigns value for loop counter
        with open(str(cwd) + '/script/script_content/csvs/Residues.csv', newline='') as Residues_file:
        #   Opens file containing Residue data using built in CSV module
            reader = csv.reader(Residues_file)
            for row in reader:
            #   Reads through each row containing Residue data
                for residue in row:
                    residue_edited = str(residue).replace(':', '')[1:]
                    #    Removes ":" and removes first character "/" (needed to allow data to be used in file name)
                    try:
                        clashes_function_TRP()
                    except Exception as Argument:
                        clasherror()
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        f = open(str(cwd) + '/error_log.txt', "a")
                        f.write("\n" + str(dt_string) + "\n" + "Error encountered calculating clashes with protein: " + str(protein) + "\n" + "Residue: " + str(residue) + " Failed\n" + "Error: " + str(Argument) + "\n")
                        f.close()
                    pass
                    try:
                        clashes_function_ARG()
                    except Exception as Argument:
                        clasherror()
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        f = open(str(cwd) + '/error_log.txt', "a")
                        f.write("\n" + str(dt_string) + "\n" + "Error encountered calculating clashes with protein: " + str(protein) + "\n" + "Residue: " + str(residue) + " Failed\n" + "Error: " + str(Argument) + "\n")
                        f.close()
                        pass
                    order = order + 1
                    #    Adds counter (used in format of file name to ensure the correct order is maintained)
        try:
            output()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/action_log.txt', "a")
            f.write(str(dt_string) + "\n" + "Completed analysis of protein: " + str(protein) + "\n")
            # Records the completion time of each protein
            f.close()
        except Exception as Argument:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            f = open(str(cwd) + '/error_log.txt', "a")
            f.write("\n" + str(dt_string) + "\n" + "Error encountered while producing output file of protein: " + str(protein) + "\n" + "Error: " + str(Argument) + "\n")
            f.close()
            pass
        #try:
            #clear_files()
        #except Exception:
            #sys.exit(1)
        #try:
            #create_files()
        #except Exception:
            #sys.exit(1)
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
f = open(str(cwd) + '/action_log.txt', "a")
f.write(str(dt_string) + "\n" + "Analysis complete\n")
# Records a final note for the time when analysis was completed 
f.close()
with open(str(cwd) + '/running/running.txt', 'w') as running:
    with redirect_stdout(running):
        print("True")
