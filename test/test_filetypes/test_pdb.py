from pathlib import Path

import pytest

from molio.filetypes.pdb import PDB
from molio.structure.atom import Atom

EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "example_files"
EXAMPLE_PDB = EXAMPLE_DIR / "ala_water.pdb"


def make_residue_atom(element, x, y, z, serial, resname="HOH", resid=1, chain="A"):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    atom.add_index(serial)
    atom.add_residue_information(resname=resname, resid=resid, chain=chain)
    atom.add_atom_type(element)
    return atom


def test_read_missing_file_raises():
    with pytest.raises(AssertionError):
        PDB().from_file(str(EXAMPLE_DIR / "does_not_exist.pdb"))


def test_read_example_pdb_atoms():
    pdb = PDB()
    pdb.from_file(str(EXAMPLE_PDB))
    atoms = pdb.structure.atoms
    assert pdb.structure.nat == 4
    assert [a.element for a in atoms] == ["N", "C", "O", "H"]
    assert {a.resname for a in atoms} == {"ALA", "HOH"}
    assert atoms[0].chain == "A"


def test_write_pdb_has_one_atom_record_per_atom(tmp_path):
    pdb = PDB()
    pdb.from_structure([
        make_residue_atom("O", 1.5, -2.0, 0.25, serial=1),
        make_residue_atom("H", 0.0, 1.0, 0.0, serial=2),
        make_residue_atom("H", 1.0, 0.0, 0.0, serial=3),
    ])
    out = tmp_path / "water.pdb"
    pdb.to_file(str(out))

    lines = out.read_text().splitlines()
    atom_lines = [line for line in lines if line.startswith("ATOM")]
    assert len(atom_lines) == 3
    assert lines[0].startswith("TITLE")


def test_write_pdb_coordinates_in_pdb_columns(tmp_path):
    pdb = PDB()
    pdb.from_structure([make_residue_atom("O", 1.5, -2.0, 0.25, serial=1)])
    out = tmp_path / "one.pdb"
    pdb.to_file(str(out))

    atom_line = next(line for line in out.read_text().splitlines() if line.startswith("ATOM"))
    assert float(atom_line[30:38]) == pytest.approx(1.5)
    assert float(atom_line[38:46]) == pytest.approx(-2.0)
    assert float(atom_line[46:54]) == pytest.approx(0.25)
    assert atom_line[76:78].strip() == "O"


def test_write_pdb_residue_and_serial(tmp_path):
    pdb = PDB()
    pdb.from_structure([make_residue_atom("N", 0, 0, 0, serial=7, resname="ALA", resid=3, chain="B")])
    out = tmp_path / "res.pdb"
    pdb.to_file(str(out))

    atom_line = next(line for line in out.read_text().splitlines() if line.startswith("ATOM"))
    assert int(atom_line[6:11]) == 7
    assert atom_line[17:20] == "ALA"
    assert atom_line[21] == "B"
    assert int(atom_line[22:26]) == 3
