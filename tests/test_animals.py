# -*- coding: utf-8 -*-

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

"""
Test file for animal properties
"""

from biosim.animals import Herbivore, Carnivore, Vulture
from biosim.simulation import BioSim
from biosim.geography import Jungle, Ocean, Mountain, Desert, Savannah

import random


def test_init():
    """
    Test that the init method works for both carnivores and herbivores.
    """
    carn = Carnivore(3, 40)
    herb = Herbivore(2, 27)

    assert carn.weight == 40
    assert carn.age == 3

    assert herb.weight == 27
    assert herb.age == 2


def test_ageing():
    """
    Test that age increases by one when when ageing method is called.
    Ageing method is defined in super-class Animal and is equally inherit
    in both Herbivore class and Carnivore class.
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
    Test that herbivores moves when supposed to.
    """

    Herbivore.param_dict['mu'] = 1
    top_cell = Jungle()
    bottom_cell = Jungle()
    right_cell = Jungle()
    left_cell = Jungle()

    herbivore = Herbivore(1, 300)
    target_cell = herbivore.migrate(top_cell, bottom_cell, left_cell,
                                    right_cell)
    assert type(target_cell).__name__ == 'Jungle'
    Herbivore.param_dict['mu'] = 0.25


def test_move_towards_cell_without_other_herbivores():
    """
    Checks that it is more likely for a herbivore to go to a jungle cell
    without other Herbivores than a cell with other herbivores.

    This also holds carnivores. Both move functions take into account the
    number of animals of same species in the cells when calculating the
    probability to move.
    """

    top_cell = Jungle()
    top_cell.present_herbivores.append(Herbivore(1, 15))
    top_cell.present_herbivores.append(Herbivore(1, 15))
    top_cell.present_herbivores.append(Herbivore(1, 15))

    right_cell = Jungle()
    bottom_cell = Ocean()
    left_cell = Ocean()
    herb = Herbivore(1, 300)

    right_counter = 0
    top_counter = 0
    for _ in range(100):
        outcome = herb.migrate(top_cell, bottom_cell, left_cell, right_cell)
        if outcome == right_cell:
            right_counter += 1

        if outcome == top_cell:
            top_counter += 1

    assert right_counter > top_counter


def test_carnivore_move():
    """
    Tests that a carnivore is inclined to move towards a cell containing
    herbivores.
    """
    top_cell = Jungle()
    top_cell.present_herbivores.append(Herbivore(1, 15))
    top_cell.present_herbivores.append(Herbivore(1, 15))
    top_cell.present_herbivores.append(Herbivore(1, 15))

    right_cell = Jungle()
    bottom_cell = Ocean()
    left_cell = Ocean()
    carn = Carnivore(1, 300)

    right_counter = 0
    top_counter = 0

    for _ in range(100):
        outcome = carn.migrate(top_cell, bottom_cell, left_cell, right_cell)
        if outcome == right_cell:
            right_counter += 1

        if outcome == top_cell:
            top_counter += 1

    assert top_counter > right_counter


def test_mountain_and_water_impassable():
    """
    Test that animals cannot move through mountains or water
    """
    test_map = 'OOOOO\nOMMMO\nOMJMO\nOMMMO\nOOOOO'
    sim = BioSim(island_map=test_map, ini_pop=[
        {"loc": (2, 2),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0},
                 {"species": "Herbivore", "age": 7, "weight": 15.0},
                 {"species": "Carnivore", "age": 7, "weight": 15.0}]}],
                 seed=random.random())
    sim.simulate(10)
    assert len(sim.map.array_map[1, 1].present_herbivores) == 0
    assert len(sim.map.array_map[1, 1].present_carnivores) == 0
    assert len(sim.map.array_map[1, 2].present_herbivores) == 0
    assert len(sim.map.array_map[1, 2].present_carnivores) == 0
    assert len(sim.map.array_map[1, 3].present_herbivores) == 0
    assert len(sim.map.array_map[1, 3].present_carnivores) == 0
    assert len(sim.map.array_map[2, 1].present_herbivores) == 0
    assert len(sim.map.array_map[2, 1].present_carnivores) == 0
    assert len(sim.map.array_map[2, 3].present_herbivores) == 0
    assert len(sim.map.array_map[1, 3].present_carnivores) == 0
    assert len(sim.map.array_map[3, 1].present_herbivores) == 0
    assert len(sim.map.array_map[3, 1].present_carnivores) == 0
    assert len(sim.map.array_map[3, 2].present_herbivores) == 0
    assert len(sim.map.array_map[3, 2].present_carnivores) == 0
    assert len(sim.map.array_map[3, 3].present_herbivores) == 0
    assert len(sim.map.array_map[3, 3].present_carnivores) == 0


def test_water_mountain_impassable():
    """
    Tests that carnivore or herbivores cannot enter cells of Ocean biome or
    Mountain biome.
    """

    top_cell = Ocean()
    bottom_cell = Mountain()
    right_cell = Mountain()
    left_cell = Ocean()

    herbi = Herbivore(1, 100)

    outcome = herbi.migrate(top_cell, bottom_cell, left_cell, right_cell)
    assert outcome is None


def test_eating():
    """
    Test that eating works as it should for the Herbivore class.
    That it returns correct new food available in cell, and that it gains
    weight according to beta * F.
    """
    herb = Herbivore(3, 35)
    assert herb.eat(300) == 290
    assert herb.weight == 44
    assert herb.eat(7) == 0
    assert herb.weight == 50.3


def test_maximum_weight():
    """ Test that no animals can surpass their maximum weight with default
    values. These are calculated by hand from
    w + F * beta - eta * (w + F * beta) = w """
    herb = Herbivore(3, 171)
    herb.eat(300)
    herb.lose_weight()
    assert herb.weight == 171

    carn = Carnivore(3, 262.5)
    carn.weight += 37.5  # maximum weight a carnivore can gain in one year
    carn.lose_weight()
    assert carn.weight == 262.5


def test_mating_and_weight():
    """
    Test the mating function, and that there is no offspring if offsprings
    weight surpasses the weight of the mother. This tests the super-class
    method, and therefore tests for both herbivores and carnivores since it
    inherits.
    """
    test_herb = Herbivore(1, 100)
    test_herb.breeding(100)
    assert test_herb.breeding(100) is not None

    test_herb2 = Herbivore(1, 5)
    assert test_herb2.breeding(100) is None


def test_death():
    """
    Test that an animal dies if its fitness is 0.
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
    """
    herb_list = [Herbivore(100, 50), Herbivore(1, 15), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    Herbivore.new_parameters({'eta': 0.05})
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


def test_hunting_stops_when_full_and_returns_left_overs():
    """
    Tests that a carnivore stops killing when its full.
    """
    herb_list = [Herbivore(100, 35), Herbivore(100, 35), Herbivore(4, 35)]
    hunter = Carnivore(3, 50)
    hunter.new_parameters({'DeltaPhiMax': 0.01})
    assert hunter.hunt(herb_list) == 20  # Also tests if it returns leftovers
    assert hunter.param_dict['DeltaPhiMax'] == 0.01
    assert hunter.weight > 50
    herb_list.sort(key=lambda x: x.phi)
    assert not herb_list[0].alive
    assert not herb_list[1].alive
    assert herb_list[2].alive


def test_weight_loss():
    """
    Test that the weight loss method works as intended.
    """
    herb = Herbivore(3, 20)
    assert herb.weight == 20
    herb.lose_weight()
    assert herb.weight == 19


def test_propensity():
    """ Test that the propensity is calculated correctly for both animals """
    jgl = Jungle()
    jgl.available_food = 100
    jgl.present_herbivores.append(Herbivore(3, 20))
    jgl.present_herbivores.append(Herbivore(2, 15))
    jgl.present_carnivores.append(Carnivore(2, 20))
    carn = Carnivore(2, 40)
    herb = Herbivore(4, 53)

    assert abs(carn._propensity_carn(jgl) - 1.419) < 0.001
    assert abs(herb._propensity_herb(jgl) - 28.032) < 0.001


def test_vulture_breeding():
    """ Test that the vultures breed with high probability """
    Vulture.new_parameters({'gamma': 1})
    vult = Vulture(3, 100)
    assert vult.breeding(2) is not None
    Vulture.new_parameters({'gamma': 0.9})


def test_vulture_scavange():
    """ Test that the vultures gain weight from scavenging """
    vult = Vulture(3, 20)
    assert vult.weight == 20
    vult.scavenge(20)
    assert vult.weight > 20


def test_vulture_can_be_in_mountain():
    """ Test that a vulture can be added to a mountain biome """
    mountain_map = 'OOO\nOMO\nOOO'
    test = BioSim(island_map=mountain_map, ini_pop=[], seed=2)
    test.add_population([{'loc': (1, 1),
                          'pop': [{'species': 'Vulture', 'age': 1,
                                  'weight': 10}]}])
    assert len(test.map.array_map[1, 1].present_vultures) == 1


def test_vulture_prefers_left_overs():
    """ Test that a vulture prefers moving to a biome with left overs """
    vult = Vulture(2, 13)
    jgl = Jungle()
    dst = Desert()
    svn = Savannah()
    mtn = Mountain()
    dst.left_overs = 200

    dst_counter = 0
    other_counter = 0
    for _ in range(10):
        if vult.migrate(svn, mtn, jgl, dst) == dst:
            dst_counter += 1
        else:
            other_counter += 1

    assert dst_counter > other_counter



