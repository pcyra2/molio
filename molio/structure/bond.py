from molio.structure.atom import Atom

class Bond:
    atom1: int
    atom2: int
    length: float

    def __init__(self, at1: int, at2: int) -> None:
        self.atom1 = at1
        self.atom2 = at2

    def set_length(self, length: float) -> None:
        self.length = length

    def calculate_bond(self, structure: list[Atom]) -> float:
        """
        Calculate bond length

        Args:
            structure (list[Atom]): List of atom objects to get coordinates of atoms.
        """
        a = structure[self.atom1]
        b = structure[self.atom2]

        ax, ay, az = float(a.x), float(a.y), float(a.z)
        bx, by, bz = float(b.x), float(b.y), float(b.z)

        dx = ax - bx
        dy = ay - by
        dz = az - bz
        self.length = (dx * dx + dy * dy + dz * dz) ** 0.5
        return  self.length