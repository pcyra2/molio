import pytest

from molio.filetypes.xyz import XYZ
from molio.structure.atom import Atom
from molio.structure.structure import Structure


def make_atom(element, x, y, z):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    return atom


def water_atoms(shift=0.0):
    return [make_atom("O", shift, 0, 0),
            make_atom("H", shift, 1, 0),
            make_atom("H", shift + 1, 0, 0)]


def test_from_structure_keeps_the_same_structure_object():
    structure = Structure()
    structure.add_atoms(water_atoms())
    xyz = XYZ()
    xyz.from_structure(structure)
    assert xyz.structure is structure


def test_from_structure_builds_structure_from_list():
    xyz = XYZ()
    xyz.from_structure(water_atoms())
    assert isinstance(xyz.structure, Structure)
    assert xyz.structure.nat == 3


def test_from_structure_ignores_unsupported_type():
    xyz = XYZ()
    xyz.from_structure("not a structure")
    assert not hasattr(xyz, "structure")


def test_update_coordinates_from_list():
    xyz = XYZ()
    xyz.from_structure(water_atoms())
    xyz.update_coordinates(water_atoms(shift=5.0))
    assert xyz.structure.atoms[0].coords() == pytest.approx((5.0, 0.0, 0.0))
    assert xyz.structure.atoms[2].coords() == pytest.approx((6.0, 0.0, 0.0))


def test_update_coordinates_from_structure():
    xyz = XYZ()
    xyz.from_structure(water_atoms())
    new = Structure()
    new.add_atoms(water_atoms(shift=-2.0))
    xyz.update_coordinates(new)
    assert xyz.structure.atoms[0].coords() == pytest.approx((-2.0, 0.0, 0.0))


def test_update_coordinates_without_structure_fails():
    xyz = XYZ()
    with pytest.raises(AttributeError):
        xyz.update_coordinates(water_atoms())


def test_base_class_reading_is_not_implemented():
    from molio.filetypes.filetypes import StructrueFile
    base = StructrueFile()
    with pytest.raises(NotImplementedError):
        base.from_file("anything.xyz")
    with pytest.raises(NotImplementedError):
        base.to_file("anything.xyz")
