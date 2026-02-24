# ChimeraX Amino-Acid Substitution Pipeline

This repository contains a ChimeraX-driven pipeline to evaluate residue tolerance for amino‑acid substitutions in proteins. It combines ChimeraX structural calculations (SASA and clash counts) with sequence‑level codon checks and generates ranked residue lists that likely to tolerate bulky substitutions.

## Pipeline

1. **Build input lists** (`input_file.py`)
   - Reads `Protein list.csv` and scans local `.pdb` and `.fna` files in `pdb/`.
   - Extracts chain IDs and PDB identifiers, writes `script/input/input.csv`.
   - Builds `script/input/codon.txt` by extracting codon sequences from `.fna`.

2. **Run ChimeraX analysis** (`script.py`)
   - Opens each PDB via ChimeraX, selects the target chain, and measures SASA.
   - Saves residue names and SASA to `script/script_content/sasa/*.defattr`.
   - Iterates through residues, swaps each to TRP/ARG, and writes clash counts to
     `script/script_content/residues_trp/` and `script/script_content/residues_arg/`.
   - Triggers the post‑processing scripts (`pandas_script.py`, `pandas2.py`).

3. **Post-process outputs** (`pandas_script.py`, `pandas2.py`)
   - Converts ChimeraX `.defattr` files to CSV.
   - Combines SASA, clash counts, and residue names.
   - Aligns residue names with codon-derived amino acids (sanity check).
   - Filters/filters residues and writes ranked outputs.

4. **Progress display** (`script1.py`)
   - Reads `running/running.txt` and `script/script_content/Protein_name/name.txt`
     to show a live terminal status during processing.

## Required Inputs

At minimum, the pipeline expects the following files and folders **relative to the
repository root**:

- `Protein list.csv`
  - A CSV containing one or more protein identifiers (one row with comma‑separated
    names or multiple rows; the scripts iterate all cells).
- `pdb/`
  - One or more PDB files: `*.pdb` (used to locate chains and for ChimeraX analysis).
  - One or more nucleotide files: `*.fna` (used to extract codon sequences).
- `running/running.txt`
  - A text file used by `script1.py` for UI status. The ChimeraX script overwrites
    this file during execution.
- `script/`
  - `script.py` expects to run under ChimeraX with the substructure below:
    - `script/input/` (generated inputs like `input.csv` and `codon.txt`).
    - `script/script_content/` (temporary outputs and intermediate files).
    - `script/subscripts/` containing `input_file.py`, `pandas_script.py`,
      `pandas2.py`, and `script1.py`.

> **Note:** The scripts derive paths using `sys.argv[0]` and assume the
> `script/` directory structure above. If you run them from another location,
> adjust paths or mirror the expected layout.

## Outputs

Primary results are written to:

- `best_residues/raw_data/<protein>.csv`
  - Combined data per residue: residue index, name, SASA exposure, TRP/ARG clashes,
    sanity check columns, and clash sums.
- `best_residues/modified_data/<protein>.csv`
  - Filtered and sorted residues (best candidates near top) based on:
    - low clash counts,
    - high SASA exposure,
    - and sequence sanity checks.

Intermediate / auxiliary outputs:

- `script/script_content/sasa/*.defattr` (ChimeraX attribute outputs)
- `script/script_content/csvs/attrcalc.csv` and `Residues.csv`
- `script/script_content/Clashes/*.txt`
- `script/script_content/codons/codon2.txt`
- `action_log.txt` and `error_log.txt`

## How to Run

1. Ensure the required input files and folders exist (see **Required Inputs**).
2. Launch ChimeraX and run `script.py` from within the ChimeraX environment.
   - The script calls the other Python helpers automatically.

Example (inside ChimeraX Python console):

```python
run(session, "open /path/to/repo/script/script.py")
```

## Notes and Assumptions

- Only the **first chain** detected for a protein is analyzed.
- Clash thresholds and filtering are hard-coded in `pandas2.py`:
  - drops residues with clash sum > 3
  - drops residues with exposure < 20
  - trims the last 20 residues of the sequence
- If the codon-derived sequence and PDB-derived sequence do not align, the
  pipeline records a warning in `error_log.txt` and flags the sanity check.

## Script Map

- `input_file.py`: Build `input.csv` and `codon.txt` from `Protein list.csv` and `pdb/`.
- `script.py`: Main ChimeraX driver (SASA + clashes + orchestration).
- `pandas_script.py`: Convert SASA `.defattr` to CSV + residue list.
- `pandas2.py`: Merge, sanity check, filter, and rank residues.
- `script1.py`: CLI progress display for long runs.
