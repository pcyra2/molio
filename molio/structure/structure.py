from molio.structure.atom import Atom
from molio.structure.bond import Bond
from molio.structure.angle import Angle

import numpy

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

    def update_coordinates(self,
                           atoms: list[Atom]) -> None:
        """
        Updates the coordinates of the atoms in the structure.

        Args:
            atoms (list[Atom]): List of atoms that have the new coordinates.
        """
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


    def translate_structure(self,
                            x: int = 0,
                            y:int = 0,
                            z: int = 0) -> None:
        """
        Translates the structure in the x,y,z coordinates.

        Args:
            x (int, optional): x coordinate of the structure. Defaults to 0.
            y (int, optional): y coordinate of the structure. Defaults to 0.
            z (int, optional): z coordinate of the structure. Defaults to 0.
        """
        for atom in self.atoms:
            if x != 0:
                atom.translate_x(x)
            if y != 0:
                atom.translate_y(y)
            if z != 0:
                atom.translate_z(z)

    def rotate_structure(self,
                         angle: float,
                         axis: tuple[float, float, float] = (0, 0, 1),
                         ) -> None:
        """
        Rotates the structure around a specific axis.

        Args:
            angle (float, optional): angle of the rotation in degrees. Defaults to 0.
            axis (tuple[float, float, float], optional): axis of the rotation. Defaults to the z axis (0, 0, 1).
        """
        vec = numpy.asarray(axis, dtype=float)
        norm_vec = numpy.linalg.norm(vec)
        if norm_vec == 0:
            raise ValueError("Axis vector cannot be zero")
        vec = vec / norm_vec
        angle_rad = numpy.radians(angle)

        cos_theta = numpy.cos(angle_rad)
        sin_theta = numpy.sin(angle_rad)

        for atom in self.atoms:
            point = numpy.asarray(atom.coords(), dtype=float)
            new_point = (point * cos_theta +
                         numpy.cross(vec, point) * sin_theta +
                         vec * numpy.dot(vec, point) * (1 - cos_theta))
            atom.update_coordinates(x=new_point[0], y=new_point[1], z=new_point[2])


    def _coord_array(self) -> numpy.ndarray:
        """
        Extracts the coordinates of the atoms in the structure.

        Returns:
            arr (numpy.ndarray): Array of coordinates of the atoms in the structure.
        """
        arr = numpy.zeros(shape=(self.nat,3) , dtype=float)
        for i, atom in enumerate(self.atoms):
            arr[i, :] = atom.coords()
        return arr


    def add_structure(self, structure2: Structure) -> None:
        """
        Adds a structure to the existing structure.

        Args:
            structure2 (Structure): Structure to be added.
        """
        final_index = self.atoms[-1].index
        s2_start_index = structure2.atoms[0].index
        s2_nat = structure2.nat

        for i, atom in enumerate(structure2.atoms): # Updates the index of atoms.
            ind = atom.index
            if ind is not None:
                atom.add_index(final_index + ind - s2_start_index + 1 ) # Accounts for if structure 2 does not start at 0.
            else:
                atom.add_index(final_index + i + 1)

        self.atoms += structure2.atoms
        self.nat += s2_nat



    # def _compute_bonds(self, max_bond_length: dict):
    # TODO