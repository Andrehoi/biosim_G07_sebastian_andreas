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
    common as well as actions. Each animal has weight, age and fitness
    properties. I also keeps track of if the animals has moved this year,
    if it is alive and what biomes it can stay in.
    """
    param_dict = {
        'w_birth': 0,
        'sigma_birth': 0,
        'beta': 0,
        'eta': 0,
        'a_half': 0,
        'phi_age': 0,
        'w_half': 0,
        'phi_weight': 0,
        'mu': 0,
        'lambda_animal': 0,
        'gamma': 0,
        'zeta': 0,
        'xi': 0,
        'omega': 0,
        'F': 0,
        'DeltaPhiMax': 0
    }

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
            DeltaPhiMax: Maximum difference in fitness between carnivore
            and herbivore

        :return:
        """
        for iterator in parameters:
            if iterator in cls.param_dict:
                cls.param_dict[iterator] = parameters[iterator]

            else:
                raise ValueError("This parameter is not defined for this "
                                 "animal")

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
        self.phi = 0
        self.calculate_fitness()
        self.alive = True
        self.has_fed = False
        self.has_bred = False
        self.has_moved = False
        self.has_aged = False
        self.has_lost_weight = False
        self.has_pot_died = False
        self.legal_biomes = ['Mountain', 'Ocean', 'Desert', 'Savannah',
                             'Jungle']

    def ageing(self):
        """
        Ages the animal by one year.
        :return:
        """
        self.age += 1

    def _sigmodial_plus(self, x, x_half, phi):
        """ Used to calculated fitness """
        return 1 / (1 + exp(phi * (x - x_half)))

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
            self.phi = self._sigmodial_plus(self.age,
                                            self.param_dict['a_half'],
                                            self.param_dict['phi_age']) * \
                       self._sigmodial_minus(self.weight,
                                             self.param_dict['w_half'],
                                             self.param_dict['phi_weight'])

    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.
        :return:
        """
        move_prob = self.param_dict['mu'] * self.phi

        if move_prob <= random.random():
            e_top = top_cell.available_food / (((len(
                top_cell.present_herbivores) + 1) * self.param_dict['F']))
            print(e_top)

            e_bottom = bottom_cell.available_food / (((len(
                bottom_cell.present_herbivores) + 1) * self.param_dict['F']))

            e_left = left_cell.available_food / (((len(
                left_cell.present_herbivores) + 1) * self.param_dict['F']))

            e_right = right_cell.available_food / (((len(
                right_cell.present_herbivores) + 1) * self.param_dict['F']))

            prop_top = exp(self.param_dict['lambda_animal'] * e_top)
            prop_bottom = exp(self.param_dict['lambda_animal'] * e_bottom)
            prop_left = exp(self.param_dict['lambda_animal'] * e_left)
            prop_right = exp(self.param_dict['lambda_animal'] * e_right)

            sum_prop = prop_top + prop_right + prop_bottom + prop_left
            top_prob = prop_top / sum_prop
            bottom_prob = prop_bottom / sum_prop
            left_prob = prop_left / sum_prop
            right_prob = prop_right / sum_prop

            number = random.random()
            if 0 <= number < top_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return top_cell

            if top_prob <= number < top_prob + bottom_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return bottom_cell

            if top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                    left_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return left_cell

            if top_prob + bottom_prob + left_prob <= number < 1:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return right_cell

    def breeding(self, n_animals_in_cell):
        """
        Calculates the probability of animal having an offspring if multiple
        animals are in the cell. Potentially creates a new animal with
        weight decided from a gaussian distribution. The mother animal loses
        weight relative to the wight of the offspring times a constant xi.
        :return: None if no animal is born, or a dict with newborn parameters
        """

        if self.weight < self.param_dict['zeta'] * \
                (self.param_dict['w_birth'] + self.param_dict['sigma_birth']):
            return

        else:
            prob_of_birth = self.param_dict['gamma'] * \
                            self.phi * (n_animals_in_cell - 1)

            if random.random() <= prob_of_birth:
                birth_weight = random.gauss(self.param_dict['w_birth'],
                                            self.param_dict['sigma_birth'])

                self.weight -= birth_weight * self.param_dict['xi']

                if type(self).__name__ == 'Herbivore':
                    print('Herbivore born')
                    return Herbivore(0, birth_weight)

                if type(self).__name__ == 'Carnivore':
                    print('Carnivore born')
                    return Carnivore(0, birth_weight)

    def lose_weight(self):
        """
        Subtracts the yearly weight loss of an animal based on weight loss
        constant eta.
        :return:
        """
        self.weight -= self.param_dict['eta'] * self.weight
        self.calculate_fitness()

    def potential_death(self):
        """
        Calculates the probability of an animal dying depending on its
        fitness. Potentially kills the animal.
        :return:
        """
        if self.phi == 0:
            self.alive = False

        else:
            death_probability = self.param_dict['omega'] * (1 - self.phi)
            rng = random.random()

            self.alive = rng >= death_probability


class Herbivore(Animal):
    """
    Class describing herbivore behaviour.
    Cannot move into mountain biomes or ocean biomes.
    """

    param_dict = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40,
        'phi_age': 0.2,
        'w_half': 10,
        'phi_weight': 0.1,
        'mu': 0.25,
        'lambda_animal': 1,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10,
    }

    def __init__(self, age, weight):
        super().__init__(age, weight)
        self.legal_biomes = ['Desert', 'Savannah', 'Jungle']

    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.
        :return:
        """
        move_prob = self.param_dict['mu'] * self.phi

        if move_prob <= random.random():
            e_top = top_cell.available_food / (((len(
                top_cell.present_herbivores) + 1) * self.param_dict['F']))

            e_bottom = bottom_cell.available_food / (((len(
                bottom_cell.present_herbivores) + 1) * self.param_dict['F']))

            e_left = left_cell.available_food / (((len(
                left_cell.present_herbivores) + 1) * self.param_dict['F']))

            e_right = right_cell.available_food / (((len(
                right_cell.present_herbivores) + 1) * self.param_dict['F']))

            prop_top = exp(self.param_dict['lambda_animal'] * e_top)
            prop_bottom = exp(self.param_dict['lambda_animal'] * e_bottom)
            prop_left = exp(self.param_dict['lambda_animal'] * e_left)
            prop_right = exp(self.param_dict['lambda_animal'] * e_right)

            sum_prop = prop_top + prop_right + prop_bottom + prop_left
            top_prob = prop_top / sum_prop
            bottom_prob = prop_bottom / sum_prop
            left_prob = prop_left / sum_prop
            right_prob = prop_right / sum_prop

            number = random.random()
            if 0 <= number < top_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return top_cell

            if top_prob <= number < top_prob + bottom_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return bottom_cell

            if top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                    left_prob:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return left_cell

            if top_prob + bottom_prob + left_prob <= number < 1:
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return right_cell

    def eat(self, food_available_in_cell):
        """
        Tries to eat amount of food F, otherwise eats whats left in the
        cell. Gains weight proportional beta*F, where beta is a constant.
        :param food_available_in_cell:
        :return: New amount of food left in cell
        """
        if food_available_in_cell >= self.param_dict['F']:
            self.weight += self.param_dict['beta'] * self.param_dict['F']
            self.calculate_fitness()
            return food_available_in_cell - self.param_dict['F']

        else:
            self.weight += self.param_dict['beta'] * food_available_in_cell
            self.calculate_fitness()
            return 0


class Carnivore(Animal):
    """
    Class describing carnivore behaviour.
    Cannot move into mountain biomes or ocean biomes.
    """
    param_dict = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 60,
        'phi_age': 0.4,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'lambda_animal': 1,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.9,
        'F': 50,
        'DeltaPhiMax': 10
    }

    def __init__(self, age, weight):
        super().__init__(age, weight)
        self.legal_biomes = ['Desert', 'Savannah', 'Jungle']

    def hunt(self, sorted_list_of_herbivores):
        """
        Tries to eat herbivores in cell, starting with herbivore with
        lowest fitness.

        Carnivores eats until it has eaten an amount F or it has tried to
        eat all herbivores in cell. Only eats amount needed of killed
        herbivore.

        Chance of successful kill increases proportionally with carnivore
        fitness, and inversely proportionally with herbivore fitness.
        :param sorted_list_of_herbivores: Takes in a list with the
        herbivores present in the cell.
        :return:
        """

        # Saves initial weight for comparison later.
        start_weight = self.weight

        # Sorts the herbivore list in ascending fitness order.
        sorted_list_of_herbivores.sort(key=lambda x: x.phi)
        kill_probability = 0

        # Calculates the probability of successful kill.
        for herbivore in sorted_list_of_herbivores:
            if self.phi <= herbivore.phi:
                kill_probability = 0

            if self.phi - herbivore.phi < self.param_dict['DeltaPhiMax']:
                kill_probability = (self.phi - herbivore.phi) / \
                                   self.param_dict['DeltaPhiMax']

            if self.phi - herbivore.phi >= self.param_dict['DeltaPhiMax']:
                kill_probability = 1

            # Checks if the carnivore kills the herbivore.
            if random.random() <= kill_probability:

                # Eats until full
                if herbivore.weight >= self.param_dict['F']:
                    self.weight += self.param_dict['beta'] * \
                                   self.param_dict['F']
                    herbivore.alive = False
                    print('ate herbivore')
                    return

                # Eats whole herbivore, and checks if its full.
                if herbivore.weight < self.param_dict['F']:
                    self.weight += self.param_dict['beta'] * herbivore.weight
                    herbivore.alive = False
                    print('ate herbivore')
                    if self.weight > start_weight + self.param_dict['beta'] * \
                            self.param_dict['F']:
                        self.weight = start_weight + self.param_dict['beta']\
                                      * self.param_dict['F']
                        return


    def migrate(self, position):
        """
        Migrates using the migrate method for animals. However if it tries
        to move into a mountain cell or ocean cell, the animal does not move.
        :return:
        """
        pass


if __name__ == '__main__':

    herb_list = [Herbivore(100, 35), Herbivore(100, 35), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    hunter.new_parameters({'DeltaPhiMax': 0.01})
    hunter.hunt(herb_list)
    print(hunter.param_dict['DeltaPhiMax'])
    print(hunter.weight)
    print(herb_list[0].phi, herb_list[0].alive)
    print(herb_list[1].phi, herb_list[1].alive)
    print(herb_list[2].phi, herb_list[2].alive)
