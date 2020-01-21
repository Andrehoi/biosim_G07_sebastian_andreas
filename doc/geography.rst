Geography
=========

Creating the map of the island
------------------------------
The island_class class creates the map of the island when called. The map is
created from a multiline string and converted into a NumPy array with class
instances in each position. The island_class class also contains the map
iterator which is used to navigate through each cell of the map.

.. autoclass:: biosim.island_class.Map
    :inherited-members:


Types of Biomes
---------------

.. autoclass:: biosim.geography.Biome
    :inherited-members:

.. autoclass:: biosim.geography.Jungle
    :inherited-members:

.. autoclass:: biosim.geography.Savannah
    :inherited-members:

.. autoclass:: biosim.geography.Desert
    :inherited-members:

.. autoclass:: biosim.geography.Ocean
    :inherited-members:

.. autoclass:: biosim.geography.Mountain
    :inherited-members:

.. autoclass:: biosim.geography.OutOfBounds
    :inherited-members: