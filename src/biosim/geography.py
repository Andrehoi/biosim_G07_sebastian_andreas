# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
File with all classes for the different kinds of biomes that the map can have.
"""


class Biome:
    """
    The Biome class stores information about the animals present in the
    cells of the island. The Biome class does not represent a specific
    biome, it is however, a super class that each type  of biome inherits
    specific properties from, e.g. the ability to contain animals and the
    ability to regrow food. The animals in a biome are sorted into two
    lists, one for herbivores(present_herbivores) and one for carnivores(
    present_carnivores).

    The global variables for the biomes are stored in a dictionary named
    param_dict. The global variables are,
    ``f_max``: Maximum amount of available food. ``f_max`` cannot be negative.
    ``alpha``: The regrowth constant which describes how much food a biome is
    able to regrow each year.
    """

    param_dict = {'f_max': 0, 'alpha': 0}

    @classmethod
    def biome_parameters(cls, parameters):
        """
        The biome_parameters method updated the values of available amount of
        food(f_max) and the regrowth constant (alpha).

        The method raises an error if there are undefined parameters within
        the dictionary or illegal values for the parameters. E.g. if the
        value of f_max is given as less than zero. Furthermore, the size of
        the dictionary param_dict may vary from biome to biome, e. g. there
        is only one element in det dictionary for the jungle biome(f_max),
        but in the Savannah both alpha and f_max is present.

        :param parameters: A dictionary containing f_max and alpha
        """
        for iterator in parameters:
            if iterator in cls.param_dict:
                if iterator == 'f_max' and parameters[iterator] < 0:
                    raise ValueError('f_max cannot be negative')

                cls.param_dict[iterator] = parameters[iterator]

            else:
                raise ValueError("This parameter is not defined for this "
                                 "biome")

    def __init__(self):
        self.available_food = 0
        self.present_carnivores = []
        self.present_herbivores = []
        self.present_vultures = []
        self.left_overs = 0

    def regrow(self):
        """
        The regrow method updates the amount of available food,
        ``available_food``, for the biome. The default regrowth of a biome
        is given as zero, however this varies from biome to biome.
        """
        self.available_food += 0


class Mountain(Biome):
    """
    The Mountain class is a sub-class of the super-class Biome. The mountain
    biome has no food for herbivores nor regrowth of  by default.
    """

    def __init__(self):
        super().__init__()


class Jungle(Biome):
    """
    The Jungle class is a sub-class of the super-class Biome. The jungle
    biome is able to contain animals and starts with a large amount of
    available food, e.g. f_max is initially defined as 800 for the jungle
    biome. Furthermore, each year when the food regrows, the amount of
    available food in the jungle becomes f_max again. Hence, the jungle
    biome does not depend on the regrowth constant alpha, only f_max.
    """
    param_dict = {'f_max': 800}

    def __init__(self):
        super().__init__()
        self.available_food = self.param_dict['f_max']

    def regrow(self):
        """
        The regrow method for the jungle biome restores the amount of
        available food to f_max when called.
        """
        self.available_food = self.param_dict['f_max']


class Savannah(Biome):
    """
    The Savannah class is a sub-class of the super-class Biome. The Savannah
    biome is able to contain animals and contains food for herbivores.
    The amount of available food in the Savannah is initially put as
    f_max = 300, which is drastically less than in the jungle biome.
    Furthermore the amount of available food in the Savannah is dependent of
    how much of the available food in the Savannah was eaten the previous year.
    """

    param_dict = {'f_max': 300, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.available_food = self.param_dict['f_max']

    def regrow(self):
        r"""
        The regrow method calculates and redefines the amount of available
        food based on the amount of available food left from the previous
        year and the regrowth factor alpha. The amount of available food
        after regrowth is calculated by the following formula:

        .. math::
            f_{new, j} = f_{old, j} + \alpha \times (f_{max} - f_{old, j})

        where ``f_{new}`` is the new amount of available food,
        ``f_{old}`` is the food left after previous year, ``alpha`` is the
        regrowth constant and ``f_{max}`` is the maximum available food in the
        Savannah.

        """
        self.available_food += self.param_dict['alpha'] \
                               * (self.param_dict[
                                      'f_max'] - self.available_food)

        if self.available_food > self.param_dict['f_max']:
            self.available_food = self.param_dict['f_max']


class Desert(Biome):
    """
    The Desert class is a sub-class of the Biome super-class. The desert may
    contain animals, however it has no food for herbivores by default.
    In the desert biome carnivores may still hunt and kill herbivores.
    """

    def __init__(self):
        super().__init__()


class Ocean(Biome):
    """
    The Ocean class is a sub-class of the Biome super-class. The Ocean may
    contain animals, however there is no food nor regrowth of food in the
    biome by default.

    """

    def __init__(self):
        super().__init__()


class OutOfBounds:
    """
    Class surrounding the map that is impassable for all animals. Cannot add
    animals to this type of cell and no animal can access it.

    These cells are created around the map by the map iterator to make sure
    noe animals can escape the map.

    The sole purpose of this biome is to trap all types of animals within
    the borders of the map. If one for example creates a fish or an
    amphibious animal it will not be able to swim beyond the borders of the
    map. It will raise 'AttributeError' if you try to move into it or put
    animals there.
    """

    def __init__(self):
        pass
