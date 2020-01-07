# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"


class Animal:
    """
    Class Animal contains characteristics the animals on Rossoya has in
    common as well as activities.
    """
    def __init__(self, parameters_animal):
        self.parameters = parameters_animal
        pass

    def ageing(self):
        """
        Ages the animal by one year.
        :return:
        """
        pass

    def calculate_fitness(self):
        """
        Calculates the animals fitness, depending on the weight and age of
        the animal. If the weight goes to zero, the fitness goes to zero.
        Otherwise it is calculated by the following function:
        :return:
        """
        pass

    def migrate(self):
        """
        Calculates the probability for an animal to move, and potenitally
        moves it. The function also calculates the probability of direction
        of movements, either east, west, north or south.
        Does not move if it tries to move into the mountains or the ocean.
        :return:
        """
        pass

    def breeding(self):
        """
        Calculates the probability of animal having an offspring if multiple
        animals are in the cell. Potentially creates a new animal.
        :return:
        """
        pass

    def lose_weight(self):
        """
        Subtracts the yearly weight loss of an animal based on weight loss
        constant eta.
        :return:
        """
        pass

    def potential_death(self):
        """
        Calculates the probability of an animal dying depending on its
        fitness. Potentially kills the animal.
        :return:
        """
        pass


class Herbivore(Animal):
    """
    Class describing herbivore behaviour.
    Cannot move into mountain boimes or ocean biomes.
    """
    def __init__(self, parameters_herbi):

        super().__init__()

    def eat(self):
        """
        Tries to eat amount of food F, otherwise eats whats left in the
        cell. Gains weight proportional beta*F, where beta is a constant.
        :return:
        """
        pass


class Carnivore(Animal):
    """
    Class describing carnivore behaviour.
    Cannot move into mountain boimes or ocean biomes.
    """
    def __init__(self, parameters_carni):
        super().__init__()

    def eat(self):
        """
        Tries to eat herbivores in cell, starting with herbivore with
        lowest fitness.

        Carnivores eats until it has eaten an amount F or it has tried to
        eat all herbivores in cell. Only eats amount needed of killed
        herbivore.

        Chance of successful kill increases proportionally with carnivore
        fitness, and inversely proportionally with herbivore fitness.
        :return:
        """
        pass
