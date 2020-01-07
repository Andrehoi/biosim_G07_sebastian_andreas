# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"


class Animal:
    """
    Class Animal contains characteristics the animals on Rossoya has in
    common as well as actions.

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
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.
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
    Cannot move into mountain biomes or ocean biomes.
    """

    w_birth = 8.0
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40
    phi_age = 0.2
    w_half = 10
    phi_weight = 0.1
    mu = 0.25
    lambda_herbivore = 1.0
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10

    @classmethod
    def new_parameters(cls, parameters):
        """
        Takes a dictionary of parameters as input. Overrides default
        parameter values. If illegal parameters of parameter values are
        input raise ValueError.

        :param parameters:
             w_birth: Average weight of offspring.
            sigma_birth: standard deviation of w_birth.
            beta: Constant that defines gained weight from food.
            eta: weigh loss constant
            a_half:
            phi_age:
            w_half:
            phi_weight:
            mu:
            lambda_herbivore:
            gamma:
            zeta:
            xi:
            omega:
            F:

        :return:
        """

    def __init__(self, parameters_herbivore):

        super().__init__()

    def migrate(self):
        """
        Migrates using the migrate method for animals. However if it tries
        to move into a mountain cell or ocean cell, the animal does not move.
        :return:
        """
        super().migrate()
        pass

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
    Cannot move into mountain biomes or ocean biomes.
    """

    w_birth = 6.0
    sigma_birth = 1.0
    beta = 0.75
    eta = 0.125
    a_half = 60
    phi_age = 0.4
    w_half = 4.0
    phi_weight = 0.4
    mu = 0.4
    lambda_carnivore = 1
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.9
    F = 50
    DeltaPhiMax = 10.0

    def __init__(self, parameters_carnivore):
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

    def migrate(self):
        """
        Migrates using the migrate method for animals. However if it tries
        to move into a mountain cell or ocean cell, the animal does not move.
        :return:
        """
        super().migrate()
        pass
