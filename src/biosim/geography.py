# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"


class Area:
    """
    Class that creates the map for the BioSim, divided into cells.
    Each cell contains food, and has a regrow capability.
    """
    def __init__(self):
        pass

    def regrow(self):
        """
        Regrows feed for the cell depending on biome.
        :return:
        """
        pass


class Mountain(Area):
    """
    Describes mountain biome. No food available for herbivores, no regrowth
    of food.
    """
    def __init__(self):
        super().__init__()


class Jungle(Area):
    """
    Describes jungle biome. Has f_max_j amount of food, and maximum regrowth.
    """
    def __init__(self):
        super().__init__()

    def regrow(self):
        pass


class Savannah(Area):
    """
    Describes savannah biome. Has f_max_s amount of food. Regrowth depends
    on food left in cell. If all the food has been consumed, regrowth is
    limited by regrowth factor alpha.
    """
    def __init__(self):
        super().__init__()

    def regrow(self):
        pass


class Dessert(Area):
    """
    Describes the desert biome. Has no food and no regrowth.
    """
    def __init__(self):
        super().__init__()


class Ocean(Area):
    """
    Describes the ocean biome. Has no food and no regrowth.
    """
    def __init__(self):
        super().__init__()
