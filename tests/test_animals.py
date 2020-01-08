# -*- coding: utf-8 -*-

"""
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from biosim.animals import Animal, Herbivore, Carnivore

"""
Test class for animal properties
"""


def test_ageing():
    """
    Test that age increases by one when when ageing method is called.
    :return:
    """

    herbivore = Herbivore(3, 12)
    assert herbivore.age == 3

    herbivore.ageing()
    assert herbivore.age == 4


def test_fitness():
    """
    Test that the fitness is calculated properly
    :return:
    """
    herbivore = Herbivore(3, 12)
    assert not herbivore.phi == 0
    assert herbivore.phi == 0.5494981150724044

def test_move():
    """
    Test that both animal types can move properly
    :return:
    """
    pass

def test_mountain_and_water_impassable():
    """
    Test that animals cannot move through mountains or water
    :return:
    """
    pass

def test_eating():
    """
    Test that eating works as it should
    :return:
    """
    pass

def test_mating_and_weight():
    """
    Test the mating function, and that there is no offspring if offsprings
    weight surpasses the weight of the mother
    :return:
    """
    pass

def test_death():
    """
    Test that an animal dies if its fitness is 0
    :return:
    """
    pass

def test_hunting():
    """
    Test the hunting capabilities of the predators. Go for the herbivore
    with lowest fitness and stop if all herbivores have been attempted
    :return:
    """
    pass
