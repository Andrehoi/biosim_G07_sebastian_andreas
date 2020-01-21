.. BioSim G.07 Sebastian & Andreas documentation master file, created by
   sphinx-quickstart on Sun Jan 12 14:52:28 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BioSim G.07 Sebastian & Andreas's documentation!
***********************************************************

Introduction:
=============
This is the exam documentation for the exam in INF200 by Sebastian Kihle and
Andreas Sandvik Hoeimyr.

The purpose of this project is to simulate and predict the development of
the ecosystem of an island. The island may consist of several types of biomes
and multiple types species of animals.

The simulation is executed by the BioSim class. BioSim calls methods from
the different other classes described in  ``Island_map``, ``Geography`` and
``Animals``.


The BioSim interface
====================
The BioSim interface is the main block of the assignment. This runs the
simulations and visualises the requested years. One may also save image files
certain years of visualization and compile a movie of them.

Initially the island simulated consists of five biomes and two species.
There is possible to add more biomes and types of animals to the ecosystem
by creating new classes for them (see ``Animals`` and ``Geography``). At
this point in time a third species of animal has been added, a vulture. This
animal is a scavenger and does not affect with the behaviour of the
other types of animals. Furthermore a biome OutOfBounds is currently in
development. The purpose of this biome is to make it possible to have
amphibious animals on the island.

The part of the code that visualizes the results is based on a project
called randvis(``https://github.com/yngvem/INF200-2019/tree/master/Project
/SampleProjects/randvis_project``). The code is mostly the same however some
variable names have substituted to make it easier to read.

BioSim class
------------

.. autoclass:: biosim.simulation.BioSim
    :inherited-members:
    :member-order: bysource

Other content
-------------
.. toctree::
   :maxdepth: 2

   animals

   geography

   examples

   installations
