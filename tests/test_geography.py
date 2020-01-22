# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
Test file for the geography of the landscape
"""

import pytest

from biosim.geography import Biome, Mountain, Ocean, Desert, Savannah, \
    Jungle, OutOfBounds


def test_regrowth_jungle():
    """
    Tests that the regrowth function always fills the available to maximum
    value.
    """

    jgl = Jungle()
    assert jgl.available_food == jgl.param_dict['f_max']

    jgl.available_food -= 50
    jgl.regrow()
    assert jgl.available_food == jgl.param_dict['f_max']


def test_regrowth_savannah():
    """
    Test that the regrowth function for Savannah adds food to cell.
    The test is run with the default parameters provided by EPAP.
    """
    # This test might fail if not used with default parameters
    Savannah.biome_parameters({'f_max': 300, 'alpha': 0.3})
    svh = Savannah()
    assert svh.available_food == svh.param_dict['f_max']

    svh.available_food -= 50
    svh.regrow()
    assert svh.available_food == 265


def test_no_regrowth_biome():
    """
    Tests that there is no available food or regrowth in the Biome
    super-class. It then follows that this holds for Desert, Ocean and
    Mountain biomes since they have no overrides.
    """
    bio = Biome()
    assert bio.available_food == 0

    bio.regrow()
    assert bio.available_food == 0


def test_no_food_in_mountains_desert_or_ocean():
    """
    Test if there is any food in the mountains or in the desert
    """
    mtn = Mountain()
    dst = Desert()
    ocn = Ocean()

    assert mtn.available_food == 0
    assert dst.available_food == 0
    assert ocn.available_food == 0


def test_set_biome_parameters():
    """
    Test that you can change the parameters for a biome.
    """
    desert = Desert()
    assert desert.param_dict['f_max'] == 0

    Desert.biome_parameters({'f_max': 125})
    dsrt = Desert()
    assert dsrt.param_dict['f_max'] == 125

    Desert.biome_parameters({'f_max': 0})


def test_out_of_bounds():
    """ Test that the OutOfBounds class cannot have any animals """
    out = OutOfBounds()
    herb = "one class instance"
    with pytest.raises(AttributeError):
        out.present_herbivores.append(herb)
