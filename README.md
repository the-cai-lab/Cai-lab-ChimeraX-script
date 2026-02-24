Finding Substitution-Tolerant Residues in Proteins using ChimeraX

Overview

This bioinformatics pipeline is designed to identify protein residues that are most likely to tolerate amino acid substitutions with minimal structural clashes. It leverages ChimeraX to calculate solvent-accessible surface areas (SASA) and assess steric clashes when substituting residues with arginine (ARG) or tryptophan (TRP). The pipeline integrates sequence data from .fna files and structural data from .pdb files to generate a ranked list of residues suitable for mutagenesis studies.

Key features:

Extract codon sequences from user-provided protein sequences.

Identify protein chains and map PDB entries to standard protein names.

Calculate solvent-accessible surface area for each residue using ChimeraX.

Perform in silico amino acid substitutions (ARG and TRP) to detect steric clashes.

Generate processed CSV files with ranked residues for mutational tolerance.

Provide logging of all actions and errors for reproducibility.

Pipeline Workflow

Preparation and Input Parsing (input_file.py)

Reads a list of standard proteins from Protein list.csv.

Extracts codon sequences from .fna files in the pdb/ directory.

Identifies protein chains and PDB file names from .pdb files.

Creates input/input.csv containing [chain, protein_name, PDB_file].

ChimeraX Structural Analysis (script.py)

Prepares workspace by clearing old output files and creating necessary subfolders.

Opens each PDB structure in ChimeraX and measures SASA for all residues (sasa_function).

Performs residue substitutions to TRP and ARG and records steric clashes (clashes_function_TRP & clashes_function_ARG).

Calls pandas2.py to convert clash and exposure data into a structured CSV.

Codon and Exposure Mapping (pandas2.py)

Assigns codons to amino acids in the protein sequence.

Merges codon sequences with SASA and clash data.

Generates a raw CSV file with residue information for each protein.

Data Processing (pandas_script.py)

Extracts residue names and exposure values from ChimeraX output.

Combines clash data from TRP and ARG substitutions.

Produces a final CSV file in best_residues/modified_data/ containing:

Residue number

Amino acid

ARG and TRP clash counts

Solvent exposure

Clash sum

Sanity check against original sequence

Residues are filtered and ranked by minimal clashes and maximal exposure.

User Interface / Monitoring (script1.py)

Provides a live terminal progress animation showing current protein and residue being analyzed.

Monitors pipeline completion via running.txt status.

Required Input Files

Protein List

Protein list.csv — A CSV file with a list of standard protein names to be analyzed.

Protein Sequences

.fna files in the pdb/ folder — GenBank-style nucleotide sequences for the proteins of interest.

Protein Structures

.pdb files in the pdb/ folder — Structural data from the Protein Data Bank.

ChimeraX Environment

The pipeline requires ChimeraX installed to perform SASA calculations and residue swaps.

Output Files

Intermediate Files

input/codon.txt — Codon sequences extracted from .fna files.

input/input.csv — Mapping of protein chain, protein name, and PDB file.

script_content/sasa/ — SASA attribute files for each protein.

script_content/residues_arg/ & script_content/residues_trp/ — Clash data for ARG and TRP substitutions.

script_content/codons/codon2.txt — Amino acid sequence mapped from codons.

script_content/csvs/ — Intermediate CSVs generated from ChimeraX attribute files.

Final Output

best_residues/raw_data/<protein>.csv — Raw merged data combining clash and exposure information.

best_residues/modified_data/<protein>.csv — Filtered and ranked list of residues most tolerant to substitution.

Columns include:

Residue: residue number

Name: amino acid

ARG: number of clashes with arginine

TRP: number of clashes with tryptophan

Exposure: solvent-accessible surface area

clash sum: total clashes

Sanity_check: validation of residue identity with .fna sequence

Logs

action_log.txt — Records start, completion, and progress of protein analyses.

error_log.txt — Captures errors encountered during the pipeline execution.

running/running.txt — Status file for UI and monitoring.
