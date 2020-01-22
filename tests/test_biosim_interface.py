# -*- coding: utf-8 -*-

"""
Test set for BioSim class interface for INF200 January 2019.

This set of tests checks the interface of the BioSim class to be provided by
the simulation module of the biosim package.

Notes:
     - The BioSim class should pass all tests in this set.
     - The tests check only that the class interface can be used, not that
       the class functions correctly. You need to write your own tests for
       that.
     - You should only run these tests on your code *after* you have
       implemented both animal and all landscape classes.
"""

__author__ = "Hans Ekkehard Plesser"
__email__ = "hans.ekkehard.plesser@nmbu.no"

import pytest
import pandas
import glob
import os
import os.path

from biosim.simulation import BioSim
from biosim.animals import Carnivore, Herbivore


def test_empty_island():
    """Empty island can be created"""
    BioSim(island_map="OO\nOO", ini_pop=[], seed=1)


def test_minimal_island():
    """Island of single jungle cell"""
    BioSim(island_map="OOO\nOJO\nOOO", ini_pop=[], seed=1)


def test_all_types():
    """All types of landscape can be created"""
    BioSim(island_map="OOOO\nOJSO\nOMDO\nOOOO", ini_pop=[], seed=1)


@pytest.mark.parametrize("bad_boundary", ["J", "S", "M", "D"])
def test_invalid_boundary(bad_boundary):
    """Non-ocean boundary must raise error"""
    with pytest.raises(ValueError):
        BioSim(
            island_map="{}OO\nOJO\nOOO".format(bad_boundary),
            ini_pop=[],
            seed=1,
        )


def test_invalid_landscape():
    """Invalid landscape type must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map="OOO\nORO\nOOO", ini_pop=[], seed=1)


def test_inconsistent_length():
    """Inconsistent line length must raise error"""
    with pytest.raises(ValueError):
        BioSim(island_map="OOO\nOJJO\nOOO", ini_pop=[], seed=1)


@pytest.mark.parametrize(
    "species, extra", [("Herbivore", {}), ("Carnivore", {"DeltaPhiMax": 0.5})]
)
def test_set_param_animals(species, extra):
    """Parameters can be set on animal classes"""

    params = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.2,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
    }
    params.update(extra)

    BioSim(island_map="O", ini_pop=[], seed=1).set_animal_parameters(
        species, params
    )

    Carnivore.new_parameters({
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


@pytest.mark.parametrize(
    "lscape, params",
    [("J", {"f_max": 100.0}), ("S", {"f_max": 200.0, "alpha": 0.1})],
)
def test_set_param_landscape(lscape, params):
    """Parameters can be set on landscape classes"""

    BioSim(island_map="O", ini_pop=[], seed=1).set_landscape_parameters(
        lscape, params
    )


def test_initial_population():
    """Test that population can be placed on construction"""

    BioSim(
        island_map="OOOO\nOJSO\nOOOO",
        ini_pop=[
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
        ],
        seed=1,
    )


@pytest.fixture
def plain_sim():
    """Return a simple island for used in various tests below"""
    return BioSim(island_map="OOOO\nOJSO\nOOOO", ini_pop=[], seed=1)


def test_add_population(plain_sim):
    """Test that population can be added to simulation"""

    plain_sim.add_population(
        [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
        ]
    )


def test_simulate(plain_sim):
    """Test that simulation can be called with visualization step values"""

    plain_sim.simulate(num_years=10, vis_years=100, img_years=100)


def test_multi_simulate(plain_sim):
    """Test that simulation can be called repeatedly"""

    plain_sim.simulate(num_years=10, vis_years=100, img_years=100)
    plain_sim.simulate(num_years=10, vis_years=100, img_years=100)


def test_get_years(plain_sim):
    """Test that number of years simulated is available"""

    plain_sim.simulate(num_years=2, vis_years=100, img_years=100)
    assert plain_sim.year == 2
    plain_sim.simulate(num_years=3, vis_years=100, img_years=100)
    assert plain_sim.year == 5


def test_get_num_animals(plain_sim):
    """Test that total number of animals is available"""

    assert plain_sim.num_animals == 0


def test_get_animals_per_species(plain_sim):
    """Test that total number of animals per species is available"""

    assert plain_sim.num_animals_per_species == {
        "Herbivore": 0,
        "Carnivore": 0,
        "Vulture": 0
    }


def test_get_animal_distribution(plain_sim):
    """Test that animal distribution is available as DataFrame"""

    plain_sim.add_population(
        [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                ],
            },
        ]
    )

    data = plain_sim.animal_distribution
    assert isinstance(data, pandas.DataFrame)
    assert len(data) == 12
    assert set(data.columns) == {"Row", "Col", "Herbivore", "Carnivore",
                                 "Vulture"}

    data.set_index(["Row", "Col"], inplace=True)
    assert data.loc[(1, 1)].Herbivore == 1
    assert data.loc[(1, 1)].Carnivore == 1
    assert data.loc[(1, 2)].Herbivore == 2
    assert data.loc[(1, 2)].Carnivore == 0

    assert data.Herbivore.sum() == 3
    assert data.Carnivore.sum() == 1


def test_set_plot_limits():
    """Test that y-axis and color limits for plots can be set."""
    BioSim(
        island_map="O",
        ini_pop=[],
        seed=1,
        ymax_animals=20,
        cmax_animals={"Herbivore": 10, "Carnivore": 20, "Vulture": 15},
    )


@pytest.fixture
def figfile_root():
    """Provide name for figfile root and delete figfiles after
    test completes"""

    ffroot = os.path.join(".", "testfigroot")
    yield ffroot
    for f in glob.glob(ffroot + "_0*.png"):
        os.remove(f)


def test_figure_saved(figfile_root):
    """Test that figures are saved during simulation"""

    sim = BioSim(
        island_map="OOOO\nOJSO\nOOOO",
        ini_pop=[],
        seed=1,
        img_base=figfile_root,
        img_fmt="png",
    )
    sim.simulate(2, vis_years=1, img_years=1)

    assert os.path.isfile(figfile_root + "_00000.png")
    assert os.path.isfile(figfile_root + "_00001.png")


def test_change_weight_simulation():
    """ Tests that a herbivore living in a jungle cell will gain weight. """

    sim = BioSim(island_map="OOO\nOJO\nOOO", ini_pop=[
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 35.0}]}], seed=0)

    assert sim.map.array_map[1, 1].present_herbivores[0].weight == 35.0
    sim.simulate(5)
    assert sim.map.array_map[1, 1].present_herbivores[0].weight != 35.0


def test_population_to_cell():
    """ Tests that you can add and store animals in a cell of the map. """

    sim = BioSim(island_map="OOO\nOJO\nOOO", ini_pop=[
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0}]}], seed=0)

    assert len(sim.map.array_map[1, 1].present_herbivores) == 1
    sim.add_population(
        [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },

        ]
    )

    assert len(sim.map.array_map[1, 1].present_herbivores) + len(
        sim.map.array_map[1, 1].present_carnivores) == 3


def test_axes_is_set_up(plain_sim):
    """ Test that the axis for the interface is set up after simulation """
    plain_sim.simulate(1)
    assert plain_sim._fig is not None
    assert plain_sim.legend_is_set_up
    assert plain_sim._heatmap_herb_ax is not None
    assert plain_sim._heatmap_carn_ax is not None
    assert plain_sim._line_graph_ax is not None


@pytest.fixture
def sim_test():
    """ Simple island with herbivores used to test """
    return BioSim(island_map='OOO\nOJO\nOOO',
                  seed=0,
                  ini_pop=[
                      {"loc": (1, 1),
                       "pop": [{"species": "Herbivore", "age": 7,
                                "weight": 40.0},
                               {"species": "Herbivore", "age": 7,
                                "weight": 40.0},
                               {"species": "Herbivore", "age": 7,
                                "weight": 40.0}]}])


def test_feeding_cycle(plain_sim):
    """ Test the feeding cycle for herbivores """
    plain_sim.add_population(
        [
            {"loc": (1, 1),
             "pop": [{"species": "Herbivore", "age": 7,
                      "weight": 40.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 40.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 40.0},
                     ]},
            {"loc": (1, 2),
             "pop": [{"species": "Herbivore", "age": 7,
                      "weight": 40.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 40.0}
                     ]}
        ]
    )

    plain_sim.feeding_cycle()
    for herbivores in plain_sim.map.array_map[1, 1].present_herbivores:
        assert herbivores.weight > 40
    for herbivores in plain_sim.map.array_map[1, 2].present_herbivores:
        assert herbivores.weight > 40


def test_breeding_cycle(plain_sim):
    """ Test that the animals have multiplied during breeding cycle. """
    plain_sim.add_population(
        [
            {"loc": (1, 1),
             "pop": [{"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     ]},
            {"loc": (1, 2),
             "pop": [{"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     ]}
        ]
    )
    plain_sim.breeding_cycle()
    plain_sim.breeding_cycle()
    plain_sim.breeding_cycle()
    assert len(plain_sim.map.array_map[1, 1].present_herbivores) > 3
    assert len(plain_sim.map.array_map[1, 2].present_carnivores) > 3


def test_aging_cycle(plain_sim):
    """ Test that all animals age by one year after aging cycle """
    plain_sim.add_population(
        [
            {"loc": (1, 1),
             "pop": [{"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     ]},
            {"loc": (1, 2),
             "pop": [{"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     ]}
        ]
    )
    plain_sim.ageing_cycle()
    for herbivore in plain_sim.map.array_map[1, 1].present_herbivores:
        assert herbivore.age == 8
    for carnivore in plain_sim.map.array_map[1, 2].present_carnivores:
        assert carnivore.age == 8


def test_weight_loss_cycle(plain_sim):
    """ Test that all animals lose weight during weight loss cycle """
    plain_sim.add_population(
        [
            {"loc": (1, 1),
             "pop": [{"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     ]},
            {"loc": (1, 2),
             "pop": [{"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     ]}
        ]
    )
    plain_sim.weight_loss_cycle()
    for herbivore in plain_sim.map.array_map[1, 1].present_herbivores:
        assert herbivore.weight == 95

    for carnivore in plain_sim.map.array_map[1, 2].present_carnivores:
        assert carnivore.weight == 87.5


def test_death_cycle(plain_sim):
    """ Tests that the death cycle works as intended. """
    Herbivore.new_parameters({'omega': 0.99})
    Carnivore.new_parameters({'omega': 0.99})
    plain_sim.add_population(
        [
            {"loc": (1, 1),
             "pop": [{"species": "Herbivore", "age": 100,
                      "weight": 0.1},
                     {"species": "Herbivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Herbivore", "age": 100,
                      "weight": 0.1},
                     ]},
            {"loc": (1, 2),
             "pop": [{"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     {"species": "Carnivore", "age": 100,
                      "weight": 1.0},
                     {"species": "Carnivore", "age": 7,
                      "weight": 100.0},
                     ]}
        ]
    )
    plain_sim.death_cycle()

    assert len(plain_sim.map.array_map[1, 2].present_carnivores) == 2
    assert len(plain_sim.map.array_map[1, 1].present_herbivores) == 1
    Herbivore.new_parameters({'omega': 0.40})
    Carnivore.new_parameters({'omega': 0.90})


def test_cannot_move_of_of_map():
    """ Test that you don't raise any errors when trying to leave the map """
    test_map = 'O'
    sim = BioSim(island_map=test_map, ini_pop=[], seed=3)
    sim.map.array_map[0, 0].present_herbivores.append(Herbivore(3, 20))
    sim.migration_cycle()

    assert len(sim.map.array_map[0, 0].present_herbivores) == 1
