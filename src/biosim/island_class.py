# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

class Map:
    """
    Class that handles and creates the island map. Converts if from a
    multiline string to an array with objects.
    """
    def __init__(self, island_multiline_sting):
        self.island_multiline_sting = island_multiline_sting


