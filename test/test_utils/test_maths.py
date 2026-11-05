import pytest

from molio.utils.maths import calc_angle, calc_distance


def test_distance_3_4_5_triangle():
    assert calc_distance((0, 0, 0), (3, 4, 0)) == pytest.approx(5.0)


def test_distance_is_symmetric_and_3d():
    assert calc_distance((1, 2, 3), (4, 6, 3)) == pytest.approx(5.0)
    assert calc_distance((4, 6, 3), (1, 2, 3)) == pytest.approx(5.0)


def test_distance_zero_for_same_point():
    assert calc_distance((2, -1, 7), (2, -1, 7)) == pytest.approx(0.0)


def test_angle_right_angle():
    assert calc_angle((1, 0, 0), (0, 0, 0), (0, 1, 0)) == pytest.approx(90.0)


def test_angle_straight_line():
    assert calc_angle((1, 0, 0), (0, 0, 0), (-1, 0, 0)) == pytest.approx(180.0)


def test_angle_60_degrees_equilateral():
    assert calc_angle((1, 0, 0), (0, 0, 0), (0.5, 3 ** 0.5 / 2, 0)) == pytest.approx(60.0)
