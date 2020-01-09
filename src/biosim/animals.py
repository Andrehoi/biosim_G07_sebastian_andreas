# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from math import exp
import random


class Animal:
    """
    Class Animal contains characteristics the animals on Rossoya has in
    common as well as actions.
    """
    w_birth = 0
    sigma_birth = 0
    beta = 0
    eta = 0
    a_half = 0
    phi_age = 0
    w_half = 0
    phi_weight = 0
    mu = 0
    lambda_herbivore = 0
    gamma = 0
    zeta = 0
    xi = 0
    omega = 0
    F = 0

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
        self.phi = 0
        self.calculate_fitness()
        self.alive = True
        self.legal_biomes = ['M', 'O', 'D', 'S', 'J']

    def ageing(self):
        """
        Ages the animal by one year.
        :return:
        """
        self.age += 1

    def _sigmodial_plus(self, x, x_half, phi):
        """ Used to calculated fitness """
        return 1/(1 + exp(phi * (x - x_half)))

    def _sigmodial_minus(self, x, x_half, phi):
        """ Used to calculate fitness """
        return 1 / (1 + exp(-phi * (x - x_half)))

    def calculate_fitness(self):
        """
        Calculates the animals fitness, depending on the weight and age of
        the animal. If the weight goes to zero, the fitness goes to zero.
        Otherwise it is calculated by the following function:
        :return:
        """
        if self.weight == 0:
            self.phi = 0
        else:
            self.phi = self._sigmodial_plus(self.age, self.a_half,
                                            self.phi_age) * \
                       self._sigmodial_minus(self.weight, self.w_half,
                                             self.phi_weight)

    def migrate(self):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.
        :return:
        """
        pass

    def breeding(self, n_animals_in_cell):
        """
        Calculates the probability of animal having an offspring if multiple
        animals are in the cell. Potentially creates a new animal with
        weight decided from a gaussian distribution. The mother animal loses
        weight relative to the wight of the offspring times a constant xi.
        :return:
        """

        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            print('no birth')
            return

        else:
            prob_of_birth = self.gamma * self.phi * (n_animals_in_cell - 1)

            if random.random() <= prob_of_birth:
                birth_weight = random.gauss(self.w_birth, self.sigma_birth)
                self.weight -= birth_weight * self.xi
                return {'species': '{0}'.format(type(self).__name__),
                        'age': 0, 'weight': birth_weight}


    def lose_weight(self):
        """
        Subtracts the yearly weight loss of an animal based on weight loss
        constant eta.
        :return:
        """
        self.weight -= self.eta * self.weight

    def potential_death(self):
        """
        Calculates the probability of an animal dying depending on its
        fitness. Potentially kills the animal.
        :return:
        """
        if self.phi == 0:
            self.alive = False

        else:
            death_probability = self.omega * (1 - self.phi)
            rng = random.random()

            self.alive = rng <= death_probability


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
    lambda_animal = 1.0
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10

    list_of_acceptable_variables = ["w_birth", "sigma_birth", "beta", "eta",
                                    "a_half", "phi_age", "w_half",
                                    "phi_weight", "mu", "lambda_animal",
                                    "gamma", "zeta", "xi", "omega", "F"]

    @classmethod
    def new_parameters(cls, parameters):
        """
        Takes a dictionary of parameters as input. Overrides default
        parameter values. If illegal parameters of parameter values are
        input raise ValueError.

        :param parameters:
            w_birth: Average weight of offspring.
            sigma_birth: Standard deviation of w_birth.
            beta: Constant that defines gained weight from food.
            eta: Weigh loss constant.
            a_half: Age component of fitness calculation.
            phi_age: Age component of fitness calculation.
            w_half: Weight component of fitness calculation.
            phi_weight: Weight component of fitness calculation.
            mu: Probability of migrating constant.
            lambda_herbivore: Direction preference dependent on food.
            gamma: Probability of birth constant.
            zeta: Birth possibility constant relative to weight.
            xi: Fraction of offspring weight the mother loses at birth.
            omega: Death probability factor.
            F: Maximum food capacity.

        :return:
        """
        for key in parameters.keys:
            if key in cls.list_of_acceptable_variables:
                cls.key = parameters[key]
            else:
                raise ValueError("This parameter is not defined for this "
                                 "animal")

    def __init__(self, age, weight):
        super().__init__(age, weight)
        self.legal_biomes = ['D', 'S', 'J']

    def migrate(self, position):
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
    lambda_animal = 1
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.9
    F = 50
    DeltaPhiMax = 10.0
    list_of_acceptable_variables = ["w_birth", "sigma_birth", "beta", "eta",
                                    "a_half", "phi_age", "w_half",
                                    "phi_weight", "mu", "lambda_animal",
                                    "gamma", "zeta", "xi", "omega", "F",
                                    "DeltaPhiMax"]

    @classmethod
    def new_parameters(cls, parameters):
        """
        Takes a dictionary of parameters as input. Overrides default
        parameter values. If illegal parameters of parameter values are
        input raise ValueError.

        :param parameters:
            w_birth: Average weight of offspring.
            sigma_birth: Standard deviation of w_birth.
            beta: Constant that defines gained weight from food.
            eta: Weigh loss constant.
            a_half: Age component of fitness calculation.
            phi_age: Age component of fitness calculation.
            w_half: Weight component of fitness calculation.
            phi_weight: Weight component of fitness calculation.
            mu: Probability of migrating constant.
            lambda_carnivore: Direction preference dependent on food.
            gamma: Probability of birth constant.
            zeta: Birth possibility constant relative to weight.
            xi: Fraction of offspring weight the mother loses at birth.
            omega: Death probability factor.
            F: Maximum food capacity.

        :return:
        """
        for key in parameters.keys:
            if key in cls.list_of_acceptable_variables:
                cls.key = parameters[key]
            else:
                raise ValueError("This parameter is not defined for this "
                                 "animal")

    def __init__(self, age, weight):
        super().__init__(age, weight)
        self.legal_biomes = ['D', 'S', 'J']

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


if __name__ == '__main__':
    dan = Carnivore(3, 34)
    print(dan.phi)
    print(dan.breeding(4))