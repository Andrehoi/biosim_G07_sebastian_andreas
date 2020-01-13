# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

import re

from biosim.geography import Mountain, Savannah, Jungle, Desert, Ocean
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.island_class import Map


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        """
                Converts the multiline string input into a numpy array of same
                dimensions.
                :param island_map:
                """
        self.map = Map(island_map)
        self.seed = seed
        self.current_year = 0

        # Adds the initial population to the map.
        self.add_population(ini_pop)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        class_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        class_dict[species].new_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        self.map.biome_dict[landscape].biome_parameters(params)

    def feeding_cycle(self):
        """ Eating cycle for each animal in the cell"""

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'Feeding')

            # cell = self.map.array_map[1, 1]
            cell.regrow()

            # Sorts each list in according to order of descending fitness.
            cell.present_herbivores.sort(key=lambda x: x.phi, reverse=True)
            cell.present_carnivores.sort(key=lambda x: x.phi, reverse=True)

            for herbivore in cell.present_herbivores:
                cell.available_food = herbivore.eat(cell.available_food)
                print('Weight of herbivore:', herbivore.weight)

            for carnivore in cell.present_carnivores:
                carnivore.hunt(cell.present_herbivores)

                alive_herbivores = [herbivore for herbivore in
                                    cell.present_herbivores if herbivore.alive]

                cell.present_herbivores = alive_herbivores

    def breeding_cycle(self):
        """ Method for yearly breeding for all animals"""

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'Breeding')

            current_herbivores = cell.present_herbivores
            newborn_herbivores = []
            for herbivore in cell.present_herbivores:
                # Checks if there is born a new animal, and potentially
                # adds it to the list of animals in the cell.
                new_herbivore = herbivore.breeding(len(
                    current_herbivores))
                if new_herbivore is not None:
                    newborn_herbivores.append(new_herbivore)

            cell.present_herbivores = current_herbivores + newborn_herbivores

            current_carnivores = cell.present_carnivores
            newborn_carnivores = []
            for carnivore in cell.present_carnivores:
                new_carnivore = carnivore.breeding((len(
                    current_carnivores)))

                if new_carnivore is not None:
                    newborn_carnivores.append(new_carnivore)

            cell.present_carnivores = current_carnivores + newborn_carnivores

    def migration_cycle(self):

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'migration')

            # Sorts each list in according to order of descending fitness.
            cell.present_herbivores.sort(key=lambda x: x.phi, reverse=True)
            cell.present_carnivores.sort(key=lambda x: x.phi, reverse=True)

            migrating_herbivores = cell.present_herbivores
            exited_herbivores = []
            for herbivore in migrating_herbivores:
                if not herbivore.has_moved:
                    target_cell = herbivore.migrate(self.map.top,
                                                    self.map.bottom,
                                                    self.map.left,
                                                    self.map.right)
                    herbivore.has_moved = True
                    if target_cell is not None:
                        target_cell.present_herbivores.append(herbivore)
                        exited_herbivores.append(herbivore)
                        print('An animal moved to ',
                              type(target_cell).__name__)

            cell.present_herbivores = [animal for animal in
                                       migrating_herbivores if animal not in
                                       exited_herbivores]

    def ageing_cycle(self):

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'ageing')

            # Ages the herbivores, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.ageing()
                print('Age:', herbivore.age)

            for carnivore in cell.present_carnivores:
                carnivore.ageing()
                print('Age:', carnivore.age)

    def weight_loss_cycle(self):

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'weight_loss')

            # The herbivores lose weight, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.lose_weight()
                print('Weight after loss:', herbivore.weight)

            for carnivore in cell.present_carnivores:
                carnivore.lose_weight()
                print('Weight after loss:', carnivore.weight)

    def death_cycle(self):

        for cell in self.map.map_iterator():
            print('Current cell:', type(cell).__name__, 'death')

            # Checks if the herbivores dies, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.potential_death()

            for carnivore in cell.present_carnivores:
                carnivore.potential_death()

            # Removes animals killed from natural causes.

            alive_herbivores = [herbivore for herbivore in
                                cell.present_herbivores if herbivore.alive]

            dead = len(cell.present_herbivores) - len(alive_herbivores)

            if dead > 0:
                print(dead, 'Herbivores died')

            cell.present_herbivores = alive_herbivores

            alive_carnivores = [carnivore for carnivore in
                                cell.present_carnivores if carnivore.alive]

            dead = len(cell.present_carnivores) - len(alive_carnivores)

            if dead > 0:
                print(dead, 'Carnivores died')

            cell.present_carnivores = alive_carnivores

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        year = 0

        while True:

            self.feeding_cycle()
            self.breeding_cycle()
            self.migration_cycle()
            self.ageing_cycle()
            self.weight_loss_cycle()
            self.death_cycle()

            for cell in self.map.map_iterator():
                for herbivore in cell.present_herbivores:
                    herbivore.has_moved = False

                for carnivore in cell.present_carnivores:
                    carnivore.has_moved = False

            # Add a year to the counter
            year += 1
            print('Current year in sim:', year)

            # Adds the amount of simulated years to the total year
            # count for the simulation.
            if year >= num_years:
                self.current_year += year
                return

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        # Unpacks the coordinates and animals to add.
        # Adds new animals to a temporary list.
        for dictionary in population:
            coordinates = dictionary['loc']
            animals_to_add = []

            # TODO: Add check for legal animal areas, and non-negative age
            #  and weight

            # Gets each new animal
            for element in dictionary['pop']:
                animals_to_add.append(element)

            # Unpacks the species value, and creates new class instance of
            # class type corresponding to species.
            # New class instance uses age and weight values from dictionary.
            for animal in animals_to_add:
                animal_class = animal['species']
                if animal_class == 'Herbivore':
                    new_animal = Herbivore(animal['age'], animal['weight'])
                    self.map.array_map[coordinates].\
                        present_herbivores.append(new_animal)
                if animal_class == 'Carnivore':
                    new_animal = Carnivore(animal['age'], animal['weight'])
                    self.map.array_map[coordinates].\
                        present_carnivores.append(new_animal)

    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        animal_counter = 0

        for cell in self.map.map_iterator():
            for _ in cell.present_herbivores:
                animal_counter += 1

            for _ in cell.present_carnivores:
                animal_counter += 1
        return animal_counter



    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        animal_dictionary = {}
        herbivore_counter = 0
        carnivore_counter = 0

        for cell in self.map.map_iterator():
            for herbivore in cell.presen_herbivores:
                herbivore_counter += 1

            for carnivore in cell.present_carnivores:
                carnivore_counter += 1



    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for
        each cell on island."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass


if __name__ == "__main__":

    k = BioSim(island_map="OOO\nOJO\nOSO\nOOO", ini_pop=[
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0}]},
        {"loc": (2, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0}]}
    ], seed=0)

    Carnivore.new_parameters({'DeltaPhiMax': 10})
    print(k.map.biome_map)

    print(k.add_population([
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 9, "weight": 45.0},
                    {"species": "Herbivore", "age": 5, "weight": 17.0},
                ],
            },
        ]
    ))
    k.simulate(10)
    print(k.num_animals)
    print('added carnivores to simulation')
    k.add_population([
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Carnivore", "age": 3, "weight": 45.0},
                    {"species": "Carnivore", "age": 2, "weight": 17.0},
                ],
            },
        ])
    print(k.current_year)

    k.simulate(10)
    print(k.num_animals)

    """
    for map_cell in k.map.map_iterator():
        print(map_cell)
    """
