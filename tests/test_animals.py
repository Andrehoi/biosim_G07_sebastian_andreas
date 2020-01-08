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
    Ageing method is defined in super-class Animal and is equally inherit
    in both Herbivore class and Carnivore class.
    :return:
    """

    herbivore = Herbivore(3, 12)
    assert herbivore.age == 3

    herbivore.ageing()
    assert herbivore.age == 4


def test_fitness():
    """
    Test that the fitness is calculated properly. Fitness is defined in the
    super-class and should be equal calculated equally. However the fitness
    parameters a_half, phi_age, w_half and phi_weight differs.
    :return:
    """
    herbivore = Herbivore(10, 0)
    assert herbivore.phi == 0

    herbivore = Herbivore(3, 12)
    assert not herbivore.phi == 0
    assert herbivore.phi == 0.5494981150724044

    carnivore = Carnivore(10, 0)
    assert carnivore.phi == 0

    carnivore = Carnivore(3, 12)
    assert not carnivore.phi == 0
    assert carnivore.phi == 0.9608342770828058


def test_lose_weight():
    """
    Tests if the method for yearly weight loss calculates correctly. The
    weight loss constant differs for the animals.
    :return:
    """

    herbivore = Herbivore(3, 12)
    carnivore = Carnivore(3, 12)

    herbivore.lose_weight()
    assert not herbivore.weight == 12
    assert herbivore.weight == 11.4

    carnivore.lose_weight()
    assert not carnivore.weight == 12
    assert carnivore.weight == 10.5

    assert not carnivore.weight == herbivore.weight


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
    herbivore = Herbivore(3, 0)
    herbivore.potential_death()

    if not herbivore.alive:
        assert True
    else:
        assert False



def test_hunting():
    """
    Test the hunting capabilities of the predators. Go for the herbivore
    with lowest fitness and stop if all herbivores have been attempted
    :return:
    """
    pass
