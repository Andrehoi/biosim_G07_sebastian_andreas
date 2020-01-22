Examples
========
Here is an example of how to run the code. There are in total three example
codes in the python directory ``examples``.

.. code-block:: python

    geogr = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJDDJJOO
               OSSSSSSSSSMMJJJDJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OOOOOOOOOOOOOOOOOOOOO"""

    geogr = textwrap.dedent(geogr)

    k = BioSim(island_map=geogr, ini_pop=[
        {"loc": (3, 3),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0}]},
        {"loc": (4, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0}
                 ]}
    ], seed=3, img_base=None)

    Carnivore.new_parameters({'DeltaPhiMax': 10})
    print(k.map.biome_map)

    print(k.add_population([
        {
            "loc": (3, 3),
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
    print(k.num_animals)
    print('Added carnivores to simulation')
    k.add_population([
        {
            "loc": (4, 1),
            "pop": [
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0},
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0},
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0},
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0}
            ],
        },

    ])
    k.simulate(20)
    k.add_population([
        {
            "loc": (2, 10),
            "pop": [
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
                {"species": "Vulture", "age": 2, "weight": 17.0},
                {"species": "Vulture", "age": 3, "weight": 45.0},
            ],
        },
    ])
    print('Added Vultures to simulation')
    k.simulate(50)
    plt.show()


