from molio.structure.atom import Atom
import numpy

class Angle:
    atom1: int
    atom2: int
    atom3: int
    angle: float

    def __init__(self, index1:int, index2:int, index3:int) -> None:
        self.atom1=index1
        self.atom2=index2
        self.atom3=index3

    def set_angle(self, value:float) -> None:
        self.angle = value

    def calculate_angle(self, atoms: list[Atom]) -> float:
        """Calculates the angle between three atoms.

        Args:
            atoms: list[Atom]

        Returns:
            angle (float): Angle between the three atoms in degrees.
        """
        a = atoms[self.atom1]
        b = atoms[self.atom2]
        c = atoms[self.atom3]

        ax, ay, az = float(a.x), float(a.y), float(a.z)
        bx, by, bz = float(b.x), float(b.y), float(b.z)
        cx, cy, cz = float(c.x), float(c.y), float(c.z)

        v1 = numpy.array([ax-bx, ay-by, az-bz])
        v2 = numpy.array([cx-bx, cy-by, cz-bz])

        cos_ang = numpy.dot(v1,v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
        ang = numpy.arccos(cos_ang)
        return numpy.degrees(ang)
