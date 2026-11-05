import pytest

from molio.structure.atom import Atom
from molio.structure.bond import Bond
from molio.structure.structure import Structure


def make_atom(element, x, y, z, index=None, charge=None):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    if index is not None:
        atom.add_index(index)
    if charge is not None:
        atom.add_charge(charge)
    return atom


def make_water(indexed=True):
    """Water: O at the origin, H at (0,1,0) and (1,0,0)."""
    atoms = [
        make_atom("O", 0, 0, 0, index=0 if indexed else None),
        make_atom("H", 0, 1, 0, index=1 if indexed else None),
        make_atom("H", 1, 0, 0, index=2 if indexed else None),
    ]
    structure = Structure()
    structure.add_atoms(atoms)
    return structure


def test_add_atoms_sets_nat_and_charge():
    atoms = [make_atom("Na", 0, 0, 0, charge=1.0),
             make_atom("Cl", 2, 0, 0, charge=-1.0)]
    structure = Structure()
    structure.add_atoms(atoms)
    assert structure.nat == 2
    assert structure.charge == pytest.approx(0.0)


def test_update_coordinates_recomputes_bonds():
    atoms = [make_atom("O", 0, 0, 0, index=0), make_atom("H", 0, 1, 0, index=1)]
    structure = Structure()
    structure.add_atoms(atoms, bonds=[Bond(0, 1)])
    assert structure.bonds[0].length == pytest.approx(1.0)

    structure.update_coordinates([make_atom("O", 0, 0, 0), make_atom("H", 0, 2, 0)])
    assert structure.atoms[1].coords() == (0, 2, 0)
    assert structure.bonds[0].length == pytest.approx(2.0)


def test_update_coordinates_rejects_element_mismatch():
    structure = make_water()
    wrong = [make_atom("N", 0, 0, 0), make_atom("H", 0, 1, 0), make_atom("H", 1, 0, 0)]
    with pytest.raises(AssertionError):
        structure.update_coordinates(wrong)


def test_update_coordinates_rejects_atom_count_mismatch():
    structure = make_water()
    with pytest.raises(AssertionError):
        structure.update_coordinates([make_atom("O", 0, 0, 0)])


def test_translate_structure_moves_every_atom():
    structure = make_water()
    structure.translate_structure(x=1, y=-1, z=2)
    assert structure.atoms[0].coords() == pytest.approx((1, -1, 2))
    assert structure.atoms[2].coords() == pytest.approx((2, -1, 2))


def test_rotate_structure_90_degrees_about_z():
    structure = Structure()
    structure.add_atoms([make_atom("C", 1, 0, 0)])
    structure.rotate_structure(90)
    assert structure.atoms[0].coords() == pytest.approx((0, 1, 0), abs=1e-12)


def test_rotate_structure_zero_axis_raises():
    structure = make_water()
    with pytest.raises(ValueError):
        structure.rotate_structure(45, axis=(0, 0, 0))


def test_coord_array_shape_and_values():
    arr = make_water()._coord_array()
    assert arr.shape == (3, 3)
    assert arr[1] == pytest.approx([0, 1, 0])


def test_geometric_centre_of_water():
    centre = make_water().calculate_center("geometric")
    assert centre == pytest.approx([1 / 3, 1 / 3, 0])


def test_default_centre_is_geometric():
    structure = make_water()
    assert structure.calculate_center() == pytest.approx(structure.calculate_center("geometric"))


def test_mass_centre_of_water():
    m_o, m_h = 15.999, 1.008
    total = m_o + 2 * m_h
    centre = make_water().calculate_center("mass")
    assert centre == pytest.approx([m_h / total, m_h / total, 0.0], rel=1e-6)


def test_mass_centre_differs_from_geometric():
    structure = make_water()
    assert not structure.calculate_center("mass") == pytest.approx(
        structure.calculate_center("geometric"))


def test_single_atom_centre_is_its_position():
    structure = Structure()
    structure.add_atoms([make_atom("Fe", 3.0, -2.0, 0.5)])
    assert structure.calculate_center("geometric") == pytest.approx([3.0, -2.0, 0.5])
    assert structure.calculate_center("mass") == pytest.approx([3.0, -2.0, 0.5])


def test_invalid_centre_mode_raises():
    with pytest.raises(ValueError):
        make_water().calculate_center("median")


def test_centre_is_returned_not_stored():
    structure = make_water()
    structure.calculate_center("mass")
    assert not any("center" in name or "centre" in name for name in vars(structure))


def test_centre_with_unknown_element_raises():
    structure = Structure()
    structure.add_atoms([make_atom("Xx", 0, 0, 0)])
    with pytest.raises(ValueError):
        structure.calculate_center("mass")


def test_add_structure_renumbers_indices():
    first = make_water()
    second = Structure()
    second.add_atoms([make_atom("C", 5, 0, 0, index=0),
                      make_atom("O", 6, 0, 0, index=1)])
    first.add_structure(second)
    assert first.nat == 5
    assert [a.index for a in first.atoms] == [0, 1, 2, 3, 4]
