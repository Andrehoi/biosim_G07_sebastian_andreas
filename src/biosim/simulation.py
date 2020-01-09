# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

import numpy as np
import re

from biosim.geography import Mountain, Savannah, Jungle, Desert, Ocean
from biosim.animals import Animal, Herbivore, Carnivore


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
        self.island_map = island_map
        self.seed = seed
        self.current_year = 0

        # Splits the multiline string and converts it into an array.
        area = self.island_map.split()
        string_map = [[cell for cell in string] for string in area]
        self.biome_map = np.array(string_map)

        # Checks that all lines in the multiline string map are as long as
        # the first line.
        reference_length = len(self.biome_map[0])
        for lines in self.biome_map:
            if len(lines) != reference_length:
                raise ValueError('All lines in map must me same length')

        # Using regular expression to check if all letters in input string
        # are defined for this island.
        if re.fullmatch(r"[OMDJS\n]+", island_map) is None:
            raise ValueError('Map contains biome not defined for this island')

        # Verifies that cells on the edge of the map are ocean biomes.
        for cell in self.biome_map[0]:
            if not cell == 'O':
                raise ValueError('Edge of map must be ocean')

        for cell in self.biome_map[-1]:
            if not cell == 'O':
                raise ValueError('Edge of map must be ocean')

        for cell in self.biome_map.T[0]:
            if not cell == 'O':
                raise ValueError('Edge of map must be ocean')

        for cell in self.biome_map.T[-1]:
            if not cell == 'O':
                raise ValueError('Edge of map must be ocean')

        # Converts array elements from strings to object instances
        self.array_map = np.array(string_map, dtype=object)
        self.biome_dict = {'O': Ocean, 'D': Desert, 'J': Jungle, 'M': Mountain,
                           'S': Savannah}

        for row in range(self.array_map.shape[0]):
            for col in range(self.array_map.shape[1]):
                self.array_map[row, col] = self.biome_dict[self.array_map[
                    row, col]]()

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
        self.biome_dict[landscape].biome_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        pass

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        for dictionary in population:
            coordinates = dictionary['loc']

            # TODO: Add check for legal animal areas
            self.array_map[coordinates].present_animals.append(dictionary[
                                                                   'pop'])
            # print(self.array_map[coordinates].present_animals)

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
    k = BioSim(island_map="OOO\nOJO\nOSO\nOOO", ini_pop=[
        {"loc": (1, 1),
        "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0}]}], seed=0)

    print(type(k.array_map[0, 0]))
    print(k.biome_map)

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
    print(k.array_map[1, 1].present_animals)
