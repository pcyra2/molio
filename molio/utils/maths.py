import numpy
"""
Some mathematical functions to aid with the parsing and computation of data.
"""

def calc_distance(p1: tuple[float, float, float],
                  p2: tuple[float, float, float]
                  )->float:
    """
    Calculates the distance between two points.
    Args:
        p1: Position of first point.
        p2: Position of second point.

    Returns:
        distance (float): Distance between two points.
    """

    ax, ay, az = p1
    bx, by, bz = p2

    dx = ax - bx
    dy = ay - by
    dz = az - bz

    return (dx * dx + dy * dy + dz * dz) ** 0.5

def calc_angle(p1: tuple[float, float, float],
               p2: tuple[float, float, float],
               p3: tuple[float, float, float]) -> float:
    """
    Calculates the angle between three points.

    Args:
        p1: Position of first point.
        p2: Position of second point.
        p3: Position of third point.

    Returns:
        angle (float): Angle between three points in degrees.
    """



    ax, ay, az = p1
    bx, by, bz = p2
    cx, cy, cz = p3

    v1 = numpy.array([ax - bx, ay - by, az - bz])
    v2 = numpy.array([cx - bx, cy - by, cz - bz])

    cos_ang = numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
    ang = numpy.arccos(cos_ang)

    return numpy.degrees(ang)
