import itertools, threading, time, sys, os
from pathlib import Path
cwd = (str(sys.argv[0][:-11]))
path_current = Path(cwd)
parent_path = path_current.parent
parent_path_2 = parent_path.parent
done = 'False'
# When done = 'True' script will end, so done is set as 'False' at the start of the script 
protein = "Finding Protein"
residue = ""
# assigns value for proetin from name.txt (see script.py)

def animate():
    # Function to produce an animation when loading       
    for c in itertools.cycle(['.    ', '..   ', '...  ', '.... ', '...  ', '..   ', '.    ']):
        if done == 'True':
            # Ends script when done == 'True' 
            break
        sys.stdout.write('\r' + str(protein) + str(residue) + " " + c)
        # Writes out the protein being analysed along with an animation 
        sys.stdout.flush()
        time.sleep(0.15)
        # Time taken between animation cycles is 0.09 seconds
    sys.stdout.write('\rDone! Finished Analysis!                         ')
    time.sleep(20)
    # Once script is finished will print the above message

def read_name():
    # Function to read through the name.txt to retrieve the protein name
    file = open(str(path_current.parent) + "/script_content/Protein_name/name.txt")
    line = file.read().replace("\n", "")
    file.close()
    protein = str(line)
    # Returns name for the protein 
    return protein


def count_current_residues():
    dir = str(parent_path) + "/script_content/residues_arg"
    list = os.listdir(dir)
    number_files = len(list)
    residues = str(number_files)
    if residues == "0":
        residues = ""
    else:
        residues = " residue: " + residues
    return residues

def count_total_residues():
    dir = str(parent_path) + "/script_content/sasa/name.defattr"
    num_lines = sum(1 for line in open(dir))
    total_res = int(num_lines) - 3
    total_res = str(total_res)
    return total_res
    


def read_running():
    # Reads through running.txt to see if value is 'True' or 'False'
    file = open(str(parent_path_2) + "/running/running.txt")
    line = file.read().replace("\n", "")
    file.close()
    done = str(line)
    return done

# Runs animation script as a separate thread
t = threading.Thread(target=animate)
t.start()

# Every 1 second reads through the protein name and checks if running.txt = 'True' or 'False' 
while done == "False":
    done = read_running()
    time.sleep(1)
    while done == "Go":
        done = read_running()
        try:
            # If name.txt has not yet been created then will print 'Finding Protein'
            protein = 'Analysing protein: ' + read_name()
        except Exception:
            pass
        try:
            residue = count_current_residues() + "/ " + count_total_residues()
        except Exception:
            pass
        time.sleep(1)


