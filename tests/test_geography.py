# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
Test file for the geography of the landscape
"""

from biosim.geography import Biome, Mountain, Ocean, Desert, Savannah, Jungle
import numpy as np


def test_regrowth_jungle():
    """
    Tests that the regrowth function always fills the available to maximum
    value.
    :return:
    """

    jgl = Jungle()
    assert jgl.available_food == jgl.f_max

    jgl.available_food -= 50
    jgl.regrow()
    assert jgl.available_food == jgl.f_max


def test_regrowth_savannah():
    """
    Test that the regrowth function for Savannah adds food to cell.
    The test is run with the default parameters provided by EPAP.
    :return:
    """
    # This test might fail if not used with default parameters
    svh = Savannah()
    assert svh.available_food == svh.f_max

    svh.available_food -= 50
    svh.regrow()
    assert svh.available_food == 265


def test_regrowth_biome():
    """
    Tests that there is no available food or regrowth in the Biome
    super-class. It then follows that this holds for Desert, Ocean and
    Mountain biomes since they have no overrides.
    :return:
    """
    bio = Biome()
    assert bio.available_food == 0

    bio.regrow()
    assert bio.available_food == 0




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