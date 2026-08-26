from molio.structure.atom import Atom
from molio.structure.bond import Bond
from molio.structure.angle import Angle

class Structure:
    """
    Contains information about a given structure.
    """
    nat: int
    charge: float
    spin: int
    atoms: list[Atom]
    bonds: list[Bond]
    angles: list[Angle]

    def __init__(self) -> None:
        pass

    def add_atoms(self,
                  atoms: list[Atom],
                  bonds: list[Bond]|None = None,
                  angles: list[Angle]|None = None) -> None:
        """
        Adds atoms to the structure

        Args:
            atoms (list[Atom]): Atoms to be added to the structure.
            bonds (list[Bond]): Bonds to be added to the structure. (Optional)
            angles (list[Angle]): Angles to be added to the structure. (Optional)
        """
        self.nat = len(atoms)
        self.atoms = atoms
        self._calculate_charge()

        if bonds is not None:
            self.bonds = bonds
            for bond in bonds:
                bond.calculate_bond(self.atoms)
        if angles is not None:
            self.angles = angles
            for angle in angles:
                angle.calculate_angle(self.atoms)

    def update_atoms(self, atoms: list[Atom]) -> None:

        assert self.nat == len(atoms)
        for i, at in enumerate(atoms):
            assert at.element == self.atoms[i].element # Check that atoms match
            self.atoms[i].update_coordinates(x=at.x, y=at.y, z=at.z)

        if hasattr(self, 'bonds'):
            for bond in self.bonds:
                bond.calculate_bond(self.atoms)
        if hasattr(self, 'angles'):
            for angle in self.angles:
                angle.calculate_angle(self.atoms)


    def _calculate_charge(self) -> None:
        """Calculates the net charge for the structure.
        This only works if the atoms have been given a charge.
        """
        chg = 0.0
        for atom in self.atoms:
            chg += atom.charge
        self.charge = chg

    # def _compute_bonds(self, max_bond_length: dict):
    # TODO