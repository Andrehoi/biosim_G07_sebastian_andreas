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
    pass
