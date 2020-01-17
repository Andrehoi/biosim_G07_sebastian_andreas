# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
Test file for the Map class
"""

from biosim.island_class import Map


def test_locations():
    """
    Test that the tiles are in the right place.
    :return:
    """
    test_map = Map('OOOO\nODJO\nOMSO\nOOOO')
    assert type(test_map.array_map[1, 1]).__name__ == 'Desert'
    assert type(test_map.array_map[1, 2]).__name__ == 'Jungle'
    assert type(test_map.array_map[2, 1]).__name__ == 'Mountain'
    assert type(test_map.array_map[2, 2]).__name__ == 'Savannah'


def test_map_iterator():
    """
    Tests that the map iterator iterates through all the cells of the map
    and returns the correct class instance for the corresponding cell.
    :return:
    """
    new_test_map = 'OOO\nODO\nOOO'

    m = Map(new_test_map)

    counter = 0
    for cell in m.map_iterator():
        if counter == 0:
            assert type(cell).__name__ == 'Ocean'

        if counter == 4:
            assert type(cell).__name__ == 'Desert'

        if counter == 6:
            assert type(cell).__name__ == 'Ocean'
        counter += 1


def test_neighbouring_cells():
    """
    Tests that the map iterator updates the four neighbouring cells for the
    current cell. If a neighbouring cell is not on the map the neighbouring
    cell should be OutOfBounds.
    :return:
    """

    new_test_map = 'OOOO\nODJO\nOMSO\nOOOO'

    m = Map(new_test_map)

    counter = 0
    for _ in m.map_iterator():
        if counter == 5:
            assert type(m.top).__name__ == 'Ocean'
            assert type(m.bottom).__name__ == 'Mountain'
            assert type(m.right).__name__ == 'Jungle'

        if counter == 12:
            assert type(m.left).__name__ == 'OutOfBounds'

        if counter == 15:
            assert type(m.bottom).__name__ == 'OutOfBounds'
            assert type(m.right).__name__ == 'OutOfBounds'

        counter += 1
