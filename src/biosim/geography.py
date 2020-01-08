# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

import numpy as np


class Biome:
    """
    Class that creates the map for the BioSim, divided into cells.
    Each cell contains food, and has a regrow capability.
    """
    def __init__(self, island_map):
        """
        Converts the multiline string input into a numpy array of same
        dimensions.
        :param island_map:
        """
        self.island_map = island_map

    def create_island_map(self):
        area = self.island_map.split()
        string_map = [[cell for cell in string] for string in area]
        array_map = np.array(string_map)
        return array_map


    def regrow(self):
        """
        Regrows feed for the cell depending on biome.
        :return:
        """
        pass


class Mountain(Biome):
    """
    Describes mountain biome. No food available for herbivores, no regrowth
    of food.
    """
    def __init__(self):
        super().__init__()


class Jungle(Biome):
    """
    Describes jungle biome. Has f_max_j amount of food, and maximum regrowth.
    """
    def __init__(self):
        super().__init__()

    def regrow(self):
        pass


class Savannah(Biome):
    """
    Describes savannah biome. Has f_max_s amount of food. Regrowth depends
    on food left in cell. If all the food has been consumed, regrowth is
    limited by regrowth factor alpha.
    """
    def __init__(self):
        super().__init__()

    def regrow(self):
        pass


class Desert(Biome):
    """
    Describes the desert biome. Has no food and no regrowth.
    """
    def __init__(self):
        super().__init__()


class Ocean(Biome):
    """
    Describes the ocean biome. Has no food and no regrowth.
    """
    def __init__(self):
        super().__init__()
