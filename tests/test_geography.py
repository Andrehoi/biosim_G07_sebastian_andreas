# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
Test file for the geography of the landscape
"""

from biosim.geography import Biome, Mountain, Ocean, Desert, Savannah, Jungle
import numpy as np


def test_init():
    """
    Tests the init of the geography class
    :return:
    """
    b = Biome(island_map="OMO\nOJO\nOSO\nOOO")
    map = b.array_map

    assert isinstance(type(map), type(np.ndarray))

    assert map[0, 1] == "M"
    assert map[2, 1] == "S"


def test_locations():
    """
    Test that the tiles are in the right place
    :return:
    """
    pass


def test_no_food_in_mountains_or_desert():
    """
    Test if there is any food in the mountains or in the desert
    :return:
    """
    pass