from pathlib import Path

import pytest

from molio.filetypes.xyz import XYZ
from molio.structure.atom import Atom
from molio.structure.structure import Structure

EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "example_files"
WATER_XYZ = EXAMPLE_DIR / "water.xyz"
WATER_TRAJ = EXAMPLE_DIR / "water_traj.xyz"


def make_atom(element, x, y, z):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    return atom


def water_atoms():
    return [make_atom("O", 0, 0, 0), make_atom("H", 0, 1, 0), make_atom("H", 1, 0, 0)]


def test_write_xyz_count_and_atom_lines(tmp_path):
    xyz = XYZ()
    xyz.from_structure(water_atoms())
    out = tmp_path / "water.xyz"
    xyz.to_file(str(out))

    lines = out.read_text().splitlines()
    assert lines[0] == "3"
    atom_lines = [line for line in lines if line.strip()][1:]
    assert len(atom_lines) == 3
    assert atom_lines[0].split("\t")[0] == "O"


def test_read_xyz_sets_atom_count_when_structure_is_set():
    xyz = XYZ()
    xyz.from_structure(Structure())
    xyz.from_file(str(WATER_XYZ))
    assert xyz.structure.nat == 3
    assert len(xyz.structure.atoms) == 3


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Known bug: XYZ.from_file builds the list as [Atom()] * nat, so all atoms share one object.",
)
def test_read_xyz_atoms_have_distinct_coordinates():
    xyz = XYZ()
    xyz.from_structure(Structure())
    xyz.from_file(str(WATER_XYZ))
    assert [a.element for a in xyz.structure.atoms] == ["O", "H", "H"]
    assert xyz.structure.atoms[1].coords() == (0.0, 1.0, 0.0)
    assert xyz.structure.atoms[2].coords() == (1.0, 0.0, 0.0)


@pytest.mark.xfail(
    strict=True,
    raises=AttributeError,
    reason="Known bug: XYZ.from_file needs self.structure to exist and does not create it.",
)
def test_read_xyz_without_preset_structure_succeeds():
    xyz = XYZ()
    xyz.from_file(str(WATER_XYZ))
    assert xyz.structure.nat == 3


def test_read_xyz_missing_file_raises():
    xyz = XYZ()
    xyz.from_structure(Structure())
    with pytest.raises(AssertionError):
        xyz.from_file(str(EXAMPLE_DIR / "missing.xyz"))


def test_from_trajectory_reads_every_frame():
    xyz = XYZ()
    xyz.from_trajectory(str(WATER_TRAJ))
    assert xyz.traj_length == 2
    assert len(xyz.trajectory) == 2
    assert all(frame.nat == 3 for frame in xyz.trajectory)


def test_from_trajectory_keeps_frames_separate():
    xyz = XYZ()
    xyz.from_trajectory(str(WATER_TRAJ))
    assert xyz.trajectory[0].atoms[1].coords() == (0.0, 1.0, 0.0)
    assert xyz.trajectory[1].atoms[1].coords() == (0.0, 2.0, 0.0)


def test_from_trajectory_sets_structure_to_last_frame():
    xyz = XYZ()
    xyz.from_trajectory(str(WATER_TRAJ))
    assert xyz.structure is xyz.trajectory[-1]
