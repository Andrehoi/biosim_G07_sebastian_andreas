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
        self.x = 0
        self.y = 0
        self.top = Ocean()
        self.bottom = Ocean()
        self.left = Ocean()
        self.right = Ocean()

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

    def map_iterator(self):
        """
        Iterates through each cell in the map. X iterates through columns in
        the map matrix, and Y iterates through rows of the map matrix.
        Yields the object in the current cell of the map.
        The yield allows the code to produce a series of cells over time,
        rather than computing them at once and sending them back like a list.
        :yields: Object in current cell.
        """
        # Starts in top left corner of map.
        x = 0
        y = 0

        # For each cell in the map yields the object.
        while True:
            if y >= 1:
                self.top = self.array_map[y-1, x]

            if y < len(self.biome_map.T[0]) - 1:
                self.bottom = self.array_map[y+1, x]

            if x >= 1:
                self.left = self.array_map[y, x-1]

            if x < len(self.biome_map[0]) - 1:
                self.right = self.array_map[y, x+1]
            # Use yield to be able to iterate through the map.
            yield self.array_map[y, x]
            x += 1

            # When it reaches the end of the row, start at the first column,
            # second row.
            if x >= len(self.biome_map[0]):
                y += 1
                x = 0

            # Stops when reaching bottom right cell of the map.
            if y >= len(self.biome_map.T[0]):
                return


if __name__ == '__main__':

    m = Map("OOOO\nOJJO\nOSSO\nOOOO")
    year_counter = 0
    while True:
        for cell in m.map_iterator():
            print(cell)
        year_counter += 1
        if year_counter >= 10:
            break