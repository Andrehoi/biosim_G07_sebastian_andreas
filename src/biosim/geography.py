# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
File with all classes for the different kinds of biomes that the map can have.
"""

import numpy as np


class Biome:
    """
    Biome stores information about the animals present in the cells of the
    map of Rossoya (array_map)
    """

    param_dict = {'f_max': 0, 'alpha': 0}

    @classmethod
    def biome_parameters(cls, parameters):
        """
        Redefines available amount of food (f_max) before a simulation and
        the regrowth factor (alpha).
        :param parameters: A dictionary containing f_max and alpha
        :return:
        """
        for iterator in parameters:
            if iterator in cls.param_dict:
                cls.param_dict[iterator] = parameters[iterator]

            else:
                raise ValueError("This parameter is not defined for this "
                                 "biome")

    def __init__(self):
        self.available_food = 0
        self.present_carnivores = []
        self.present_herbivores = []

    def regrow(self):
        """
        Regrows feed for the cell depending on biome.
        :return:
        """
        self.available_food += 0


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
    param_dict = {'f_max': 800}

    def __init__(self):
        super().__init__()
        self.available_food = self.param_dict['f_max']

    def regrow(self):
        """
        Sets the amount of food available at the start of a year as f_max.
        :return:
        """
        self.available_food = self.param_dict['f_max']


class Savannah(Biome):
    """
    Describes savannah biome. Has f_max_s amount of food. Regrowth depends
    on food left in cell. If all the food has been consumed, regrowth is
    limited by regrowth factor alpha.
    """

    param_dict = {'f_max': 300, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.available_food = self.param_dict['f_max']

    def regrow(self):
        """
        Calculates the amount of food available at the start of a year.
        This depends on the amount of food left from previous year and the
        regrowth factor alpha.
        :return:
        """
        self.available_food += self.param_dict['alpha'] * \
                               (self.param_dict['f_max'] - self.available_food)

        if self.available_food > self.param_dict['f_max']:
            self.available_food = self.param_dict['f_max']


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


class OutOfBounds:
    """
    Class surrounding map that is impassable for all animals. Cannot add
    animals to this cell and no animal can access it.

    These cells are created around the map by the map iterator to make sure
    noe animals can escape the map.
    """
    def __init__(self):
        pass
