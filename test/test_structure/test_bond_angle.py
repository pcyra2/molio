import pytest

from molio.structure.angle import Angle
from molio.structure.atom import Atom
from molio.structure.bond import Bond


def make_atom(element, x, y, z, index):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    atom.add_index(index)
    return atom


def test_bond_length_uses_atom_index_not_position():
    # Indices start at 10, so a list-position lookup would fail.
    atoms = [make_atom("C", 0, 0, 0, 10), make_atom("C", 3, 4, 0, 11)]
    bond = Bond(10, 11)
    assert bond.calculate_bond(atoms) == pytest.approx(5.0)
    assert bond.length == pytest.approx(5.0)


def test_bond_missing_index_raises():
    atoms = [make_atom("C", 0, 0, 0, 0)]
    with pytest.raises(AssertionError):
        Bond(0, 99).calculate_bond(atoms)


def test_set_bond_length_stores_value():
    bond = Bond(0, 1)
    bond.set_length(1.5)
    assert bond.length == pytest.approx(1.5)


def test_angle_right_angle_at_vertex():
    # Vertex is atom2 (index 0), with arms along x and y.
    atoms = [make_atom("O", 0, 0, 0, 0),
             make_atom("H", 0, 1, 0, 1),
             make_atom("H", 1, 0, 0, 2)]
    angle = Angle(1, 0, 2)
    assert angle.calculate_angle(atoms) == pytest.approx(90.0)
    assert angle.angle == pytest.approx(90.0)


def test_angle_straight_line_is_180():
    atoms = [make_atom("C", 1, 0, 0, 0),
             make_atom("C", 0, 0, 0, 1),
             make_atom("C", -1, 0, 0, 2)]
    assert Angle(0, 1, 2).calculate_angle(atoms) == pytest.approx(180.0)


def test_set_angle_stores_value():
    angle = Angle(0, 1, 2)
    angle.set_angle(109.5)
    assert angle.angle == pytest.approx(109.5)
