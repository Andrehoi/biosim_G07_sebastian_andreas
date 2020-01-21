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
    properties. I also keeps track of if the animals has moved, if it is
    alive and what biomes it can stay in.

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

        :param parameters: A dictionary of parameters.

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
            and herbivore.
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
        Ages the animal by one year and calls the calculate_fitness method
        to recalculate the fitness of the animal.
        """
        self.age += 1
        self.calculate_fitness()

    @staticmethod
    def _sigmodial_plus(x, x_half, phi):
        """ Used to calculated fitness """
        return 1 / (1 + exp(phi * (x - x_half)))

    @staticmethod
    def _sigmodial_minus(x, x_half, phi):
        """ Used to calculate fitness """
        return 1 / (1 + exp(-phi * (x - x_half)))

    def calculate_fitness(self):
        r"""
        Calculates the animals fitness, depending on the weight and age of
        the animal. If the weight is zero, the fitness is zero.
        Otherwise it is calculated by the following formula:

        .. math::
            \phi = q^{+} (a, a_{1/2}, \phi_{age}) \times q^{-} (w, w_{1/2},
            \phi_{weight})

        where ``a`` is the age w is the weight, ``a_{1/2}``, phi_age,
        ``w_1/2`` and ``phi_weight`` are defined in the param_dict. q^{±} is
        defined as:

        .. math::
            q^{±}(x, x_{1/2}, \phi) = \frac{1}{(1 + e^{±(x - x_{1/2})})}

        where ``x`` and ``phi`` are input variables.

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
        animals are in the cell.

        The method then potentially creates a new animal. The new animal is
        of the same class as the parent animal and its weight is decided
        from a gaussian distribution and age zero.
        The mother animal loses weight relative to the weight of the
        offspring times a constant xi. The mothers fitness is then
        recalculated with its new weight.
        However, if a animal is not born the method returns None.

        :return: None, or a class instance of same species.
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

                if isinstance(self, Herbivore):
                    self.calculate_fitness()
                    return Herbivore(0, birth_weight)

                elif isinstance(self, Carnivore):
                    self.calculate_fitness()
                    return Carnivore(0, birth_weight)

                elif isinstance(self, Vulture):
                    self.calculate_fitness()
                    return Vulture(0, birth_weight)

    def _choose_direction(self, prop_top, prop_bottom, prop_left, prop_right,
                          top_cell, bottom_cell, left_cell, right_cell):
        """
        Chooses the direction of migration for an animal.

        :param prop_top: Propensity for moving to top cell.
        :param prop_bottom: Propensity for moving to bottom cell.
        :param prop_left: Propensity for moving to left cell.
        :param prop_right: Propensity for moving to right cell.
        :return: None if cell is illegal, else, the target cell to move to.
        """
        # sum_prop is the probability of the animal migrating when it
        # migrates and should be 1.
        sum_prop = prop_top + prop_right + prop_bottom + prop_left

        # Creates 4 intervals of walking to the 4 different cells based
        # on the probability of walking to the cells.
        top_prob = prop_top / sum_prop
        bottom_prob = prop_bottom / sum_prop
        left_prob = prop_left / sum_prop

        # Checks which direction the animal chooses to move. Returns the
        # cell in the chosen direction.
        number = random.random()
        if number < top_prob:
            # Checks if the cell is in the legal biomes of the animal.
            if not type(top_cell).__name__ in self.legal_biomes:
                return None
            return top_cell

        elif top_prob <= number < top_prob + bottom_prob:
            if not type(bottom_cell).__name__ in self.legal_biomes:
                return None
            return bottom_cell

        elif top_prob + bottom_prob <= number < top_prob + bottom_prob + \
                left_prob:
            if not type(left_cell).__name__ in self.legal_biomes:
                return None
            return left_cell

        else:
            if not type(right_cell).__name__ in self.legal_biomes:
                return None
            return right_cell

    def lose_weight(self):
        """
        Subtracts the yearly weight loss of an animal based on weight loss
        constant eta and recalculates the fitness of the animal.
        """

        self.weight -= self.param_dict['eta'] * self.weight
        self.calculate_fitness()

    def potential_death(self):
        r"""
        Calculates the probability of an animal dying depending on its
        fitness. Potentially kills the animal.

        If the fitness of the animal is zero the attribute 'alive' is put to
        False and the animal dies.

        If the fitness is larger than zero a probability of death is
        calculated from the formula:

        ..:math:
            p_{death} = \omega \times (1 - \phi}

        where ``omega`` is defined in the param_dict and ``phi`` is the fitness
        of the animal.
        The function then possibly kills the animal based on p_{death}.
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

    The herbivore class is a sub-class of the Animal-class and contain mostly
    the same methods. It however, also defines specific methods for eating and
    migration.
    Furthermore the param_dict for a herbivore has different
    default values for the different parameters and does not contain
    PhiDeltaMax. The herbivore class also restricts which biome an animal
    can move into. A herbivore can't move into Ocean biomes or Mountain biomes.
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

        :param cell: A cell next to the cell the animal is in.
        :return: prop_cell: The propensity to move into a cell.
        """

        e_cell = cell.available_food / (((len(
            cell.present_herbivores) + 1) * self.param_dict['F']))

        prop_cell = exp(self.param_dict['lambda_animal'] * e_cell)

        return prop_cell

    def migrate(self, top_cell, bottom_cell, left_cell, right_cell):
        r"""
        Calculates the probability for an animal to move one cell, and
        potentially moves it. The function also calculates the probability
        of direction of movements, either east, west, north or south.

        The method first calculates the probability of moving using the
        parameter 'mu' and the fitness of the animal. By default the largest
        probability is 0.25. It then uses a random generated number to check
        if the animal moves.

        If the animal moves the propensity to move to each surrounding cell
        is calculated. The propensity to move to a cell takes into account
        how many herbivores are present in the cell and how much food is
        available. Herbivores are inclined to move towards the cell with the
        most available food. Herbivores are inclined to move towards the
        cell with the least amount of herbivores.

        The propensity to move to a cell is calculated by the following
        formula:

        .. math::
            \pi_{i->j} = e^{(\lambda \epsilon_{j})}

        where ``pi`` is the propensity to move to the cell, ``lambda`` is a
        paramter defined in the param_dict and ``epsilon`` is defined as:

        .. math::
            e_{j} = \frac{f_{j}}{((n_{j} + 1) \times F)}

        where ``f`` is the amount of available food, ``n`` is the number of
        animals of the same species and `F``` is the appetite of the animal
        as defined in the param_dict.

        Four probability intervals are created and a randomly generated number
        chooses which cell the animal moves to according to which interval
        the random number falls into. Lastly the method checks if
        the chosen cell is a legal biome for the animal and if it is the
        animal moves, else the animal does not move and remain in the cell.

        :param top_cell: The cell north of current cell.
        :param bottom_cell: The cell south of current cell.
        :param left_cell: The cell west of current cell.
        :param right_cell: The cell east of current cell.

        :return Target_cell: The target cell is the cell the animal moves to.
        """

        move_prob = self.param_dict['mu'] * self.phi

        # Uses a random number to check if the hebivore moves.
        if move_prob >= random.random():

            prop_top = self._propensity_herb(top_cell)
            prop_bottom = self._propensity_herb(bottom_cell)
            prop_left = self._propensity_herb(left_cell)
            prop_right = self._propensity_herb(right_cell)

            return self._choose_direction(prop_top, prop_bottom, prop_left,
                                          prop_right, top_cell, bottom_cell,
                                          left_cell, right_cell)

    def eat(self, food_available_in_cell):
        """
        The eat method takes the available food in the current cell as
        input. The amount of available food is defined in the biome class
        instances.
        When called the method tries to eat F amount of food, if this is not
        possible it eats what is left in the cell.
        After eating the animal gains weight proportional to beta*F, where beta
        is a parameter defined in the param_dict.

        The amount of food eaten by the animal is then subtracted from the
        amount of available food. If there is less than F amount of food
        left in cell before the eat method is called, the eat method returns 0.

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

    The Carnivore class is a sub-class of the class Animal. Most actions a
    carnivore can do is inherit from the super-class Animal, however it
    contains methods for eating(hunt) and migration. Furthermore it contains
    different default values for each parameter in the param_dict.

    The Carnivore class also restrict which biome an animal can move into or
    stay in. A carnivore can't move into Ocean biomes or Mountain biomes.
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
        r"""
        The hunt method is the eating method for the Carnivore class. When
        called for a carnivore it tries to eat the herbivores in cell,
        starting with the herbivore with the lowest fitness. The carnivore
        will eat until it has eaten an amount F or it has tried to eat all
        the herbivores in the cell.

        The hunt method has three possible outcomes depending on the
        difference in fitness between the carnivore and the herbivore it
        tries to eat.
        If the herbivore has a greater fitness than the carnivore the
        probability of successfully eating the herbivore is 0.

        If the difference in fitness for the carnivore and herbivore is
        between zero and 'DeltaPhiMax' the probability of successfully
        eating the herbivore is calculated with the following formula:

        .. math::
            p_{kill} = \frac{(\phi_{carn} - \phi_{herb})}{\Delta\Phi_{max}},

        where ``DeltaPhiMax`` is defined in the param_dict, ``Phi_carn`` is the
        fitness of the carnivore and ``Phi_herb`` is the fitness of the
        herbivore.

        The third scenario is if the difference in fitness between the
        herbivore and carnivore are larger than DeltaPhiMax the probability
        of successfully eating the herbivore is 1.

        Thereafter the hunt method modifies the weight of the carnivore,
        recalculates its fitness and
        puts the 'alive' attribute of the herbivore to False.

        The weight of the carnivore increases by beta*F if the herbivore's
        weight is equal or greater than F(50 by default). On the other hand,
        if the weight of the herbivore is less than F the carnivore eats the
        herbivore and goes on to try to kill another one. This is repeated
        until the carnivore either has eaten an amount of F or has tried to
        kill all the herbivores in the cell.
        The fitness of the carnivore is recalculated after each kill.

        :param sorted_list_of_herbivores: present herbivores sorted by fitness
        """

        # Saves initial weight for comparison later.
        start_weight = self.weight

        kill_probability = 0
        weight_of_killed_animals = 0

        for herbivore in sorted_list_of_herbivores:
            if self.phi <= herbivore.phi:
                kill_probability = 0

            elif self.phi - herbivore.phi < self.param_dict['DeltaPhiMax']:
                kill_probability = (self.phi - herbivore.phi) / \
                                   self.param_dict['DeltaPhiMax']

            else:
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
                else:

                    self.weight += self.param_dict['beta'] * herbivore.weight
                    herbivore.alive = False
                    self.calculate_fitness()

                    weight_of_killed_animals += herbivore.weight

                    left_overs = weight_of_killed_animals - self.param_dict[
                        'F']
                    if left_overs >= 0:
                        self.weight = start_weight + self.param_dict['beta']\
                                      * self.param_dict['F']
                        return left_overs

    def _propensity_carn(self, cell):
        """
        Calculates the propensity an animal has to move to a cell.

        :param cell: A cell next to the cell the animal is in.
        :return: prop_cell: The propensity to move into a cell.
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

        The method first calculates the probability of moving using the
        parameter 'mu' and the fitness of the animal. By default the largest
        probability is 0.25. It then uses a random generated number to check
        if the animal moves.

        If the animal moves the propensity to move to each surrounding cell
        is calculated. The propensity to move to a cell takes into account
        how many carnivores are present in the cell and how much food is
        available. In the case of carnivores the available food is the list
        of present_herbivores stored in the class instance in each cell.
        The propensity for a carnivore to move to a cell is calculated in
        the same way as for a herbivore.

        Carnivores are inclined to move towards the cell with the
        most herbivores. Carnivores are inclined to move towards the
        cell with the least amount of other carnivores.

        Four probability intervals are created and a randomly generated number
        chooses which cell the animal moves to according to which interval
        the random number is in. Lastly the method checks if
        the chosen cell is a legal biome for the animal and if it is the
        animal moves, else the animal does not move and remain in the cell.

        :param top_cell: The cell north of current cell.
        :param bottom_cell: The cell south of current cell.
        :param left_cell: The cell west of current cell.
        :param right_cell: The cell east of current cell.

        :return Target_cell: The target cell is the cell the animal moves to.
        """

        move_prob = self.param_dict['mu'] * self.phi
        
        # Checks if the animal moves based on the probability of moving.
        if move_prob <= random.random():

            # prop_xxx is the propensity to move to cell xxx.
            prop_top = self._propensity_carn(top_cell)
            prop_bottom = self._propensity_carn(bottom_cell)
            prop_left = self._propensity_carn(left_cell)
            prop_right = self._propensity_carn(right_cell)

            return self._choose_direction(prop_top, prop_bottom, prop_left,
                                          prop_right, top_cell, bottom_cell,
                                          left_cell, right_cell)


class Vulture(Animal):
    """
    An animal that can fly into the mountains and eats left overs from
    carnivore kills.
    Has a lot of the same parameters as a carnivore for simplicity's sake.
    """
    param_dict = {
        'w_birth': 2.0,
        'sigma_birth': 0.5,
        'beta': 0.9,
        'eta': 0.025,
        'a_half': 60,
        'phi_age': 0.4,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'lambda_animal': 1,
        'gamma': 0.9,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.40,
        'F': 10,
    }

    def __init__(self, age, weight):
        super().__init__(age, weight)
        self.legal_biomes = ['Desert', 'Savannah', 'Jungle', 'Mountain']

    def scavenge(self, left_overs):
        """
        Eats the left overs from carnivore kills. Left overs stay in a cell
        for a year before they rot away.

        :param left_overs: Left overs from kills
        :return: The new amount of left overs in the cell
        """

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

        :param cell: Cell to calculate propensity for.
        :return: The propensity of the cell.
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

        Vultures are inclined to move towards the cell with the most
        left overs.

        Vultures also consider how many other vultures are in the cells
        around when it migrates. It is inclined to move towards a cell with
        the least vultures. Vultures can fly into the mountains.

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

            return self._choose_direction(prop_top, prop_bottom, prop_left,
                                          prop_right, top_cell, bottom_cell,
                                          left_cell, right_cell)
