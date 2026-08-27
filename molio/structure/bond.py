from molio.structure.atom import Atom
from molio.utils.maths import calc_distance

class Bond:
    """
    Bond class

    Attributes:
        atom1 (int): First atom index
        atom2 (int): Second atom index
        length (float): Bond length
    """
    atom1: int
    atom2: int
    length: float

    def __init__(self, at1: int, at2: int) -> None:
        """
        Initialize Bond class

        Args:
            at1 (int): First atom index
            at2 (int): Second atom index
        """
        self.atom1 = at1
        self.atom2 = at2

    def set_length(self, length: float) -> None:
        """
        Sets the value of the bond length

        Args:
            length (float): Bond length
        """
        self.length = length

    def calculate_bond(self, atoms: list[Atom]) -> float:
        """
        Calculate bond length

        Args:
            atoms (list[Atom]): List of atom objects to get coordinates of atoms.
        """

        a = None
        b = None

        for atom in atoms: # This allows for the use of PDB indexing, rather than automatically starting from 0.
            if atom.index == self.atom1:
                a = atom
            if atom.index == self.atom2:
                b = atom

        assert a is not None
        assert b is not None

        self.length = calc_distance(a.coords(), b.coords())

        return  self.length