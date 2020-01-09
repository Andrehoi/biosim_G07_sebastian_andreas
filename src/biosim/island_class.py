# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from biosim.geography import Mountain, Savannah, Jungle, Desert, Ocean
import numpy as np
import re


class Map:
    """
    Class that handles and creates the island map. Converts if from a
    multiline string to an array with objects.
    """
    def __init__(self, island_multiline_sting):
        self.island_multiline_sting = island_multiline_sting

        # Splits the multiline string and converts it into an array.
        area = self.island_multiline_sting.split()
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
        if re.fullmatch(r"[OMDJS\n]+", island_multiline_sting) is None:
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

        return

if __name__ == '__main__':

    m = Map("OOO\nOJO\nOOO")
    print(m.array_map)
    print(m.biome_map)