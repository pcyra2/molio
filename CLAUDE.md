# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

There is no build, lint, or CI configuration in the repo. Run everything from the repository root so `molio` imports from the working tree.

- Run all tests: `python -m pytest`
- Run one test file: `python -m pytest test/test_filetypes/test_pdb.py`
- Run one test: `python -m pytest test/test_filetypes/test_pdb.py::test_pdb_read`

Runtime dependencies are `numpy` and `tqdm`. The code uses `X|None` annotations evaluated at runtime, so Python 3.10+ is required (the environment used is 3.12).

Current state: the test suite does not pass. `test/test_filetypes/test_pdb.py` fails at collection because line 7 passes the return value of `Atom.set_atom()` (which is `None`) into `Structure.add_atoms()`. `EXAMPLE_PDB` is also an empty string, and `test_pdb_write` is an empty stub.

## Architecture

The package is `molio/`, a wrapper for reading and writing molecular structure files. It has four layers:

1. **Core model (`molio/structure/`)**. `Atom` holds element, coordinates, charge, residue/chain info, and an `index`. `Structure` owns a list of atoms plus optional `bonds` and `angles`. `Bond` and `Angle` store atom *indices*, not list positions, and look up atoms by matching `atom.index` against `structure.atoms` each time they are computed. Anything that wants bond or angle values must therefore set `atom.index` consistently (PDB uses the file serial number; XYZ uses the 0-based line position).

2. **File formats (`molio/filetypes/`)**. `StructrueFile` (the misspelling is in the code and is what the subclasses import) is the base class. It holds the parsed `self.structure` and provides `from_structure`, `update_coordinates`, and the `NotImplementedError` stubs for `from_file`/`to_file`. Subclasses are:
   - `PDB`: full read and write, plus `fetch()` to download from RCSB. Writing goes through `_format_atom`, which emits fixed-width PDB columns.
   - `XYZ`: read and write, plus `from_trajectory()`, which fills `self.trajectory` with one `Structure` per frame.
   - `Mol2`: a stub with no parsing.

   The usual flow is: parse lines into `Atom` objects, call `Structure.add_atoms()`, then transform the structure in memory and write it back out with the same format class.

3. **Residue table (`molio/structure/proteins.py`)**. `AMINO_ACIDS` maps residue names to `AminoAcid` records (parent name, polar flag, charge at pH 7). It includes protonation/state variants such as HID/HIE/HIP, LYN, ASH/GLH, and CYM/CYX. Nothing in the parsers or `Structure` uses it yet.

4. **Utilities (`molio/utils/`)**. `print_center` produces the banner output the parsers print while reading. `maths.py` has `calc_distance` and `calc_angle` (degrees), used by `Bond` and `Angle`. `variables.TERM_SIZE` is read once at import time.

Note that `Structure.add_structure` and `Structure.update_coordinates` rely on the same `atom.index` convention, so it is safest to keep indices consistent with the file they came from.

## Known issues (verified by running small inputs)

- `XYZ.from_file()` builds its atom list as `[Atom()] * nat`, which repeats one object. Every atom is overwritten by the last line read, so all atoms end up at the same coordinates. The same pattern appears as `[Atom] * nat` in `from_trajectory()`, though there each slot is replaced.
- `XYZ.from_file()` expects `self.structure` to already exist and raises `AttributeError` otherwise. Set it with `from_structure()` first, or initialise a `Structure`.
- `PDB.from_file()` allocates `[Atom] * (nat - 1)`, where `nat` is the last serial number. For a normal file with serials 1..N this raises `IndexError` on the final atom.
