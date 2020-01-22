# -*- coding: utf-8 -*-

import textwrap
from biosim.simulation import BioSim
import matplotlib.pyplot as plt

"""
Example run for the BioSim interface
"""

__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

if __name__ == '__main__':
    geogr = """\
               OOOO
               OMJO
               OSDO
               OOOO"""

    simple_island = textwrap.dedent(geogr)
    c_max = {'Herbivore': 100, 'Carnivore': 50, 'Vulture': 10}

    k = BioSim(island_map=simple_island, ini_pop=[
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0}]},
        {"loc": (2, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 ]}
    ], seed=3, img_base=None, ymax_animals=200, cmax_animals=c_max)

    print(k.add_population([
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 9, "weight": 45.0},
                {"species": "Herbivore", "age": 5, "weight": 17.0},
                {"species": "Herbivore", "age": 9, "weight": 45.0},
                {"species": "Herbivore", "age": 5, "weight": 17.0}
            ],
        },
    ]
    ))
    k.simulate(50)
    print(k.num_animals, 'live animals at year', k.year)
    print('Added carnivores to simulation')
    k.add_population([
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0},

            ],
        },

    ])
    k.simulate(20)
    k.add_population([
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
            ],
        },
    ])
    print('Added Vultures to simulation')
    k.simulate(130)
    print(k.num_animals, 'live animals at year', k.year)
    plt.show()
