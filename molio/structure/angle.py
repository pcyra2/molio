from molio.structure.atom import Atom
import numpy

class Angle:
    atom1: int
    atom2: int
    atom3: int
    angle: float

    def __init__(self, at1: int, at2: int, at3:int) -> None:
        """
        Initializes a bond angle.

        Args:
            at1 (int): The index of the first atom.
            at2 (int): The index of the second atom.
            at3 (int): The index of the third atom.
        """
        self.atom1 = at1
        self.atom2 = at2
        self.atom3 = at3

    def set_angle(self, value:float) -> None:
        """
        Sets the value of the angle.

        Args:
            value (float): The value of the angle. in degrees.
        """
        self.angle = value

    def calculate_angle(self, atoms: list[Atom]) -> float:
        """Calculates the angle between three atoms.

        Args:
            atoms: list[Atom]

        Returns:
            angle (float): Angle between the three atoms in degrees.
        """
        a = None
        b = None
        c = None

        for atom in atoms:  # This allows for the use of PDB indexing, rather than automatically starting from 0.
            if atom.index == self.atom1:
                a = atom
            elif atom.index == self.atom2:
                b = atom
            elif atom.index == self.atom3:
                c = atom

        assert a is not None
        assert b is not None
        assert c is not None

        ax, ay, az = float(a.x), float(a.y), float(a.z)
        bx, by, bz = float(b.x), float(b.y), float(b.z)
        cx, cy, cz = float(c.x), float(c.y), float(c.z)

        v1 = numpy.array([ax-bx, ay-by, az-bz])
        v2 = numpy.array([cx-bx, cy-by, cz-bz])

        cos_ang = numpy.dot(v1,v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
        ang = numpy.arccos(cos_ang)
        return numpy.degrees(ang)
