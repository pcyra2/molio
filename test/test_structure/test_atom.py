import pytest

from molio.structure.atom import ATOMIC_MASSES, Atom


def make_atom(element="C", x=0.0, y=0.0, z=0.0):
    atom = Atom()
    atom.set_atom(element, x, y, z)
    return atom


def test_atomic_masses_cover_periodic_table():
    assert len(ATOMIC_MASSES) == 118
    assert ATOMIC_MASSES["H"] == pytest.approx(1.008)
    assert ATOMIC_MASSES["Og"] == pytest.approx(294.0)


def test_get_atomic_mass_known_elements():
    assert make_atom("H")._get_atomic_mass() == pytest.approx(1.008)
    assert make_atom("Cl")._get_atomic_mass() == pytest.approx(35.45)


def test_get_atomic_mass_unknown_element_raises():
    with pytest.raises(ValueError):
        make_atom("Xx")._get_atomic_mass()


def test_mass_is_not_stored_on_atom():
    assert not hasattr(Atom(), "mass")
    assert make_atom("O").__dict__.get("mass") is None


def test_set_atom_and_coords():
    atom = make_atom("N", 1.0, 2.0, 3.0)
    assert atom.element == "N"
    assert atom.coords() == (1.0, 2.0, 3.0)


def test_set_atom_returns_none():
    # set_atom mutates in place; it does not return the atom.
    assert Atom().set_atom("C", 0, 0, 0) is None


def test_translate_axes():
    atom = make_atom("C", 0.0, 0.0, 0.0)
    atom.translate_x(1.0)
    atom.translate_y(2.0)
    atom.translate_z(-3.0)
    assert atom.coords() == pytest.approx((1.0, 2.0, -3.0))


def test_update_coordinates_overwrites():
    atom = make_atom("C", 1.0, 1.0, 1.0)
    atom.update_coordinates(x=4.0, y=5.0, z=6.0)
    assert atom.coords() == (4.0, 5.0, 6.0)


def test_add_index_and_default_none():
    atom = make_atom("C")
    assert atom.index is None
    atom.add_index(7)
    assert atom.index == 7


def test_add_charge_default_only_sets_charge():
    atom = make_atom("C")
    atom.add_charge(-0.5)
    assert atom.charge == pytest.approx(-0.5)
    assert atom.occ == pytest.approx(1.0)
    assert atom.beta == pytest.approx(0.0)


def test_add_charge_to_occupancy_column():
    atom = make_atom("C")
    atom.add_charge(0.25, pdb_col="occ")
    assert atom.occ == pytest.approx(0.25)


def test_add_charge_to_beta_column():
    atom = make_atom("C")
    atom.add_charge(0.75, pdb_col="beta")
    assert atom.beta == pytest.approx(0.75)


def test_add_residue_information_and_prefix():
    atom = make_atom("O")
    atom.add_residue_information(resname="HOH", resid=2, chain="A")
    atom.change_prefix("HETATM")
    assert (atom.resname, atom.resid, atom.chain) == ("HOH", 2, "A")
    assert atom.pdb_prefix == "HETATM"


def test_echo_format():
    assert make_atom("H", 0.5, 1.0, -2.0).echo() == "H 0.5 1.0 -2.0"
