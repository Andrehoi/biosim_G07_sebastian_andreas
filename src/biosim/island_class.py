# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from biosim.geography import Mountain, Savannah, Jungle, Desert, Ocean, \
    OutOfBounds
import numpy as np
import re


class Map:
    """
    The Map class takes a multiline string as input and creates a numpy
    array of it.
    The numpy array will contain one letter in each position and is saved as
    biome_map.

    The biome_map is then used to create a numpy array of class instances
    named array_map. This is done with a dictionary. Each position in the
    biome_map is a single letter string. In the dictionary(biome_dict) the
    string is a key with a class instance as a value. The class instances in
    the dictionary are the different classes defined in the geography file.
    E. g. if a position in the biome_map is 'J' it will be
    the class Jungle in the array_map.

    The Map class also checks that the input string fulfills certain criteria.
    Each row of the multiline string must have the same amount of letters,
    else a ValueError is raised.
    The string can only contain the letters which has corresponding classes.
    This is checked using regular expression. As of now the only legal
    letters are J, D, S, O and M, corresponding to the biomes Jungle,
    Desert, Savannah, Ocean and Mountain. If there are different letters in
    the input string a ValueError is raised.
    It checks that the string gives a map where all edge cells are ocean,
    if not a ValueError is raised. See ``Examples`` for an example of an
    accepted input string.

    :param : A multiline string with letters J, S, D, O, M
    """
    def __init__(self, island_multiline_sting):
        self.island_multiline_sting = island_multiline_sting
        self.x = 0
        self.y = 0
        self.top = OutOfBounds()
        self.bottom = OutOfBounds()
        self.left = OutOfBounds()
        self.right = OutOfBounds()

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
        The map_iterator method iterates through each cell in array_map.
        self.x is used to iterate through columns in array_map, and self.y is
        used to
        iterate through the rows in self.array_map(numpy array with class
        instances in each position).
        Yields the object in the current cell of the map.
        The yield allows the code to produce a series of cells over time,
        rather than computing them at once and sending them back like a list.

        Each time the map_iterator is called the values of x and y are reset
        to zero. The iterator then yields each cell until it has yielded
        each cell in the array_map.

        The map_iterator saves the surrounding cells around the current
        cell. If the current cell is on the edge of the map,
        the neighbouring cell outside the map is set to be OutOfBounds cell.
        These neighbouring cells are stored and used when animals migrate.

        :yields: Object in current cell.

        """
        # Starts in top left corner of map.
        self.x = 0
        self.y = 0

        # For each cell in the map yields the object.
        while True:
            if self.y >= 1:
                self.top = self.array_map[self.y-1, self.x]
            else:
                self.top = OutOfBounds()

            if self.y < len(self.biome_map.T[0]) - 1:
                self.bottom = self.array_map[self.y+1, self.x]
            else:
                self.bottom = OutOfBounds()

            if self.x >= 1:
                self.left = self.array_map[self.y, self.x-1]
            else:
                self.left = OutOfBounds()

            if self.x < len(self.biome_map[0]) - 1:
                self.right = self.array_map[self.y, self.x+1]
            else:
                self.right = OutOfBounds()
            # Use yield to be able to iterate through the map.
            yield self.array_map[self.y, self.x]
            self.x += 1

            # When it reaches the end of the row, start at the first column,
            # second row.
            if self.x >= len(self.biome_map[0]):
                self.y += 1
                self.x = 0

            # Stops when reaching bottom right cell of the map.
            if self.y >= len(self.biome_map.T[0]):
                return
