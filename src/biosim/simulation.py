# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

import numpy as np
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
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

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

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        year = 0
        while True:
            # cell = self.map.map_iterator()
            cell = Jungle()
            cell.regrow()
            cell_list = cell.present_animals
            for animal in cell_list:
                animal.eat(cell.available_food)
                cell.present_animals.append(animal.breeding())
                # migration
                animal.ageing()
                animal.lose_weight()
                animal.potential_death()
            year += 1
            if year >= num_years:
                self.current_year += year
                print(self.current_year)
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
                        present_animals.append(new_animal)
                if animal_class == 'Carnivore':
                    new_animal = Carnivore(animal['age'], animal['weight'])
                    self.map.array_map[coordinates].\
                        present_animals.append(
                        new_animal)


    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        pass

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        pass

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for
        each cell on island."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass


if __name__ == "__main__":
    k = BioSim(island_map="OOO\nOJO\nOOO", ini_pop=[
        {"loc": (1, 1),
        "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0}]}], seed=0)

    print(type(k.map.array_map[0, 0]))
    print(k.map.biome_map)

    print(k.add_population([
            {
                "loc": (2, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 15.0},
                    {"species": "Carnivore", "age": 4, "weight": 8.0},
                ],
            },
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20.0},
                    {"species": "Carnivore", "age": 2, "weight": 5.0},
                ],
            },
        ]
    ))
    print(k.map.array_map[1, 1].present_animals)
    print(k.map.array_map[2, 1].present_animals)
    k.simulate(5)
    k.simulate(3)
    print(k.current_year)
