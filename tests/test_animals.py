# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from biosim.animals import Animal, Herbivore, Carnivore

"""
Test file for animal properties
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
    assert abs(herbivore.phi - 0.5494) < 0.0001

    carnivore = Carnivore(10, 0)
    carnivore.new_parameters({'phi_age': 0.4, 'a_half': 60, 'w_half': 4.0,
                              'phi_weight': 0.4})
    assert carnivore.phi == 0

    carnivore = Carnivore(3, 12)
    assert not carnivore.phi == 0
    assert abs(carnivore.phi - 0.9608) < 0.00004


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

    carnivore.new_parameters({'eta': 0.125})
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
    Test that eating works as it should for the Herbivore class.
    That it returns correct new food available in cell, and that it gains
    weight according to beta * F.
    :return:
    """
    herb = Herbivore(3, 35)
    assert herb.eat(300) == 290
    assert herb.weight == 44
    assert herb.eat(7) == 0
    assert herb.weight == 50.3


def test_mating_and_weight():
    """
    Test the mating function, and that there is no offspring if offsprings
    weight surpasses the weight of the mother. This tests the super-class
    method, and therefore tests for both herbivores and carnivores since it
    inherits.
    :return:
    """
    test_herb = Herbivore(1, 100)
    test_herb.breeding(100)
    assert test_herb.breeding(100) is not None

    test_herb2 = Herbivore(1, 5)
    assert test_herb2.breeding(100) is None


def test_death():
    """
    Test that an animal dies if its fitness is 0
    :return:
    """
    herbivore = Herbivore(3, 0)
    assert herbivore.alive
    herbivore.potential_death()
    assert not herbivore.alive

    immortal_herb = Herbivore(2, 100)
    immortal_herb.potential_death()
    assert immortal_herb.alive


def test_hunting():
    """
    Test the hunting capabilities of the predators. Go for the herbivore
    with lowest fitness and stop if all herbivores have been attempted
    :return:
    """
    herb_list = [Herbivore(100, 50), Herbivore(1, 15), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    hunter.new_parameters({
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 60,
        'phi_age': 0.4,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'lambda_animal': 1,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.9,
        'F': 50,
        'DeltaPhiMax': 10
    })
    hunter.new_parameters({'DeltaPhiMax': 0.5})
    hunter.hunt(herb_list)
    assert hunter.weight > 50
    assert not herb_list[0].alive
    assert herb_list[1].alive
    assert herb_list[2].alive
    hunter.new_parameters({'DeltaPhiMax': 10})


def test_hunting_stops_when_full():
    """
    Tests that a carnivore stops killing when its full.
    :return:
    """
    herb_list = [Herbivore(100, 35), Herbivore(100, 35), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    hunter.new_parameters({'DeltaPhiMax': 0.01})
    hunter.hunt(herb_list)
    assert hunter.param_dict['DeltaPhiMax'] == 0.01
    assert hunter.weight > 50
    herb_list.sort(key=lambda x: x.phi)
    assert not herb_list[0].alive
    assert not herb_list[1].alive
    assert herb_list[2].alive


def test_weight_loss():
    herb = Herbivore(3, 20)
    assert herb.weight == 20
    herb.lose_weight()
    assert herb.weight == 19


