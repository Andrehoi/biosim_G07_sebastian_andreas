# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
File with the animal classes, such as Herbivore and Carnivore.
"""

from math import exp
import random


class Animal:
    """
    Class Animal contains characteristics the animals on Rossoya have in
    common as well as actions. Each animal has weight, age and fitness
    properties. I also keeps track of if the animals has moved this year,
    if it is alive and what biomes it can stay in.

    The class takes age and weight as input and checks that the value of
    these are not negative. Then based on the value of the age and weight
    calculate the initial fitness of the animal(phi).

    The animal class is a super-class for all animals on the island and
    therefore has no biome constrictions except for the OutOfBounds biome.

    The animal class has a dictionary param_dict that contains all global
    parameters for animals on the island. These variables are zero by default.
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
        Takes a dictionary of parameters as input. It overrides the default
        parameter values. If illegal parameters or parameter values are
        input it raises a raise ValueError. E. g. the parameter eta must be
        between zero and one.

        :param: A dictionary of parameters.
        The different parameters for an animal are the following:

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
        """

        for iterator in parameters:
            if iterator in cls.param_dict:
                if iterator == 'eta' and parameters[iterator] >= 1:
                    raise ValueError('eta must be less or equal to 1')
                if iterator == 'DeltaPhiMax' and parameters[iterator] <= 0:
                    raise ValueError('DeltaPhiMax must be larger than zero')
                if parameters[iterator] < 0:
                    raise ValueError('{} cannot be negative'.format(iterator))
                cls.param_dict[iterator] = parameters[iterator]

            else:
                raise ValueError("This parameter is not defined for this "
                                 "animal")

    def __init__(self, age, weight):

        if age < 0:
            raise ValueError('The animal cannot have a negative age')
        else:
            self.age = age

        if weight < 0:
            raise ValueError('The animal cannot have a negative weight')
        else:
            self.weight = weight

        self.phi = 0
        self.calculate_fitness()

        self.alive = True
        self.has_moved = False

        self.legal_biomes = ['Mountain', 'Ocean', 'Desert', 'Savannah',
                             'Jungle']

    def ageing(self):
        """
        Ages the animal by one year.
        :return:
        """
        self.age += 1
        self.calculate_fitness()

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

    def breeding(self, n_animals_in_cell):
        """
        Calculates the probability of animal having an offspring if multiple
        animals are in the cell. Potentially creates a new animal with
        weight decided from a gaussian distribution. The mother animal loses
        weight relative to the wight of the offspring times a constant xi.
        :return: None if no animal is born, or a newborn class instance of
        same animal species.
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
                    self.calculate_fitness()
                    return Herbivore(0, birth_weight)

                if type(self).__name__ == 'Carnivore':
                    self.calculate_fitness()
                    return Carnivore(0, birth_weight)

                if type(self).__name__ == 'Vulture':
                    self.calculate_fitness()
                    return Vulture(0, birth_weight)

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

    def _propensity_herb(self, cell):
        """
        Calculates the propensity an animal has to move to a cell.
        :param cell:
        :return:
        """

        e_cell = cell.available_food / (((len(
            cell.present_herbivores) + 1) * self.param_dict['F']))

        prop_cell = exp(self.param_dict['lambda_animal'] * e_cell)

        return prop_cell


    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.

        Herbivores are inclined to move towards the cell with the most of
        available fodder.

        Herbivores are inclined to move towards the cell with the least
        amount of herbivores.

        :param top_cell: The cell north of current cell.
        :param bottom_cell: The cell south of current cell.
        :param left_cell: The cell west of current cell.
        :param right_cell: The cell east of current cell.

        :return: Target_cell. The target cell is the cell the animal moves to.
        """

        move_prob = self.param_dict['mu'] * self.phi

        # Uses a random number to check if the hebivore moves.
        if move_prob >= random.random():

            prop_top = self._propensity_herb(top_cell)
            prop_bottom = self._propensity_herb(bottom_cell)
            prop_left = self._propensity_herb(left_cell)
            prop_right = self._propensity_herb(right_cell)

            # sum_prop is the probability of the animal migrating when it
            # migrates and should be 1.
            sum_prop = prop_top + prop_right + prop_bottom + prop_left

            # Creates 4 intervals of walking to the 4 different cells based
            # on the probability of walking to the cells.
            top_prob = prop_top / sum_prop
            bottom_prob = prop_bottom / sum_prop
            left_prob = prop_left / sum_prop
            right_prob = prop_right / sum_prop

            # Checks which direction the animal chooses to move. Returns the
            # cell in the chosen direction.
            number = random.random()
            if number < top_prob:
                # Checks if the cell is in the legal biomes of the animal.
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return top_cell

            if top_prob <= number < top_prob + bottom_prob:
                if not type(bottom_cell).__name__ in self.legal_biomes:
                    return None
                return bottom_cell

            if top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                    left_prob:
                if not type(left_cell).__name__ in self.legal_biomes:
                    return None
                return left_cell

            if top_prob + bottom_prob + left_prob <= number < 1:
                if not type(right_cell).__name__ in self.legal_biomes:
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

        kill_probability = 0
        weight_of_killed_animals = 0

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
                    self.calculate_fitness()
                    return

                # Eats whole herbivore, and checks if its full.
                if herbivore.weight < self.param_dict['F']:

                    self.weight += self.param_dict['beta'] * herbivore.weight
                    herbivore.alive = False
                    self.calculate_fitness()

                    weight_of_killed_animals += herbivore.weight

                    left_overs = weight_of_killed_animals - self.param_dict[
                        'F']
                    if left_overs >= 0:
                        self.weight = start_weight + self.param_dict['beta']\
                                      * self.param_dict['F']
                        return

    def _propensity_carn(self, cell):
        """
        Calculates the propensity an animal has to move to a cell.
        :param cell:
        :return:
        """

        herb_weight = 0
        for herbivore in cell.present_herbivores:
            herb_weight += herbivore.weight

        e_cell = herb_weight / (((len(cell.present_carnivores) + 1)
                                * self.param_dict['F']))

        prop_cell = exp(self.param_dict['lambda_animal'] * e_cell)

        return prop_cell

    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.

        Carnivores are inclined to move towards the cell with the most
        herbivores measured in weight.

        Carnivores also consider how many other carnivores are in the cells
        around when it migrates. It is inclined to move towards a cell with
        the least carnivores.
        
        :param top_cell: The cell north of current cell.
        :param bottom_cell: The cell south of current cell.
        :param left_cell: The cell west of current cell.
        :param right_cell: The cell east of current cell.
        
        :return: The cell the animal migrates to (target_cell).
        """

        move_prob = self.param_dict['mu'] * self.phi
        
        # Checks if the animal moves based on the probability of moving.
        if move_prob <= random.random():

            # prop_xxx is the propensity to move to cell xxx.
            prop_top = self._propensity_carn(top_cell)
            prop_bottom = self._propensity_carn(bottom_cell)
            prop_left = self._propensity_carn(left_cell)
            prop_right = self._propensity_carn(right_cell)

            # sum_prop is the probability of the animal migrating when it
            # migrates and should be 1.
            sum_prop = prop_top + prop_right + prop_bottom + prop_left

            # Creates 4 intervals of walking to the 4 different cells based
            # on the probability of walking to the cells.
            top_prob = prop_top / sum_prop
            bottom_prob = prop_bottom / sum_prop
            left_prob = prop_left / sum_prop
            right_prob = prop_right / sum_prop

            # Checks which direction the animal chooses to move. Returns the
            # cell in the given direction.
            number = random.random()
            if 0 <= number < top_prob:
                # Checks if the cell in a direction is in the legal biomes
                # of the animal.
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return top_cell

            if top_prob <= number < top_prob + bottom_prob:
                if not type(bottom_cell).__name__ in self.legal_biomes:
                    return None
                return bottom_cell

            if top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                    left_prob:
                if not type(left_cell).__name__ in self.legal_biomes:
                    return None
                return left_cell

            if top_prob + bottom_prob + left_prob <= number < 1:
                if not type(right_cell).__name__ in self.legal_biomes:
                    return None
                return right_cell


class Vulture(Animal):
    """
    An animal that can fly and eats left overs from carnivore kills.
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
        self.legal_biomes = ['Desert', 'Savannah', 'Jungle', 'Mountain']

    def scavenge(self, left_overs):

        if left_overs >= self.param_dict['F']:
            self.weight += self.param_dict['beta'] * self.param_dict['F']
            self.calculate_fitness()
            return left_overs - self.param_dict['F']

        else:
            self.weight += self.param_dict['beta'] * left_overs
            self.calculate_fitness()
            return 0

    def _propensity_vult(self, cell):
        """
        Calculates the propensity an animal has to move to a cell.
        :param cell:
        :return:
        """

        e_cell = cell.left_overs / (((len(
            cell.present_vultures) + 1) * self.param_dict['F']))

        prop_cell = exp(self.param_dict['lambda_animal'] * e_cell)

        return prop_cell

    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        """
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.

        Carnivores are inclined to move towards the cell with the most
        herbivores measured in weight.

        Carnivores also consider how many other carnivores are in the cells
        around when it migrates. It is inclined to move towards a cell with
        the least carnivores.

        :param top_cell: The cell north of current cell.
        :param bottom_cell: The cell south of current cell.
        :param left_cell: The cell west of current cell.
        :param right_cell: The cell east of current cell.

        :return: The cell the animal migrates to (target_cell).
        """

        move_prob = self.param_dict['mu'] * self.phi

        # Checks if the animal moves based on the probability of moving.
        if move_prob <= random.random():

            # prop_xxx is the propensity to move to cell xxx.
            prop_top = self._propensity_vult(top_cell)
            prop_bottom = self._propensity_vult(bottom_cell)
            prop_left = self._propensity_vult(left_cell)
            prop_right = self._propensity_vult(right_cell)

            # sum_prop is the probability of the animal migrating when it
            # migrates and should be 1.
            sum_prop = prop_top + prop_right + prop_bottom + prop_left

            # Creates 4 intervals of walking to the 4 different cells based
            # on the probability of walking to the cells.
            top_prob = prop_top / sum_prop
            bottom_prob = prop_bottom / sum_prop
            left_prob = prop_left / sum_prop
            right_prob = prop_right / sum_prop

            # Checks which direction the animal chooses to move. Returns the
            # cell in the given direction.
            number = random.random()
            if 0 <= number < top_prob:
                # Checks if the cell in a direction is in the legal biomes
                # of the animal.
                if not type(top_cell).__name__ in self.legal_biomes:
                    return None
                return top_cell

            if top_prob <= number < top_prob + bottom_prob:
                if not type(bottom_cell).__name__ in self.legal_biomes:
                    return None
                return bottom_cell

            if top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                    left_prob:
                if not type(left_cell).__name__ in self.legal_biomes:
                    return None
                return left_cell

            if top_prob + bottom_prob + left_prob <= number < 1:
                if not type(right_cell).__name__ in self.legal_biomes:
                    return None
                return right_cell


if __name__ == '__main__':

    herb_list = [Herbivore(100, 35), Herbivore(100, 35), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    hunter.hunt(herb_list)
    print(hunter.param_dict['DeltaPhiMax'])

