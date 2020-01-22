Animals
=======
The animal class is not used in the simulation, however it contains all
methods the different types of animals have in common. Animal also contain the
param_dict, however all parameters within have a value of zero. This
param_dict is overridden in the classes for the other animals.

.. autoclass:: biosim.animals.Animal
    :inherited-members:
    :member-order: bysource

Herbivores
----------
The following code block shows the default param_dict for a herbivore.

.. code-block:: python

    param_dict = {
    'w_birth': 8.0,
    'sigma_birth': 1.5,
    'beta': 0.9,
    'eta': 0.05,
    'a_half': 40,
    'phi_age': 0.2,
    'w_half': 10,
    'phi_weight': 0.1,
    'mu': 0.25,
    'lambda_animal': 1,
    'gamma': 0.2,
    'zeta': 3.5,
    'xi': 1.2,
    'omega': 0.4,
    'F': 10,
    }

.. autoclass:: biosim.animals.Herbivore
    :members: eat, migrate

Carnivores
----------
The following code-block shows the default param_dict for carnivores.

.. code-block:: python

    param_dict = {
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
    }

.. autoclass:: biosim.animals.Carnivore
    :members: hunt, migrate

Additional animals
------------------

.. autoclass:: biosim.animals.Vulture
    :members: scavenge, migrate
