__author__ = "Yngve Mardal Moe"
import numpy as np


def _sigmoid(x):
    return 1 / (1 + np.exp(x))


class Animal:
    rng = np.random
    params = {
        "w_birth": 0.5,
        "sigma_birth": 0.1,
        "phi_age": 0.3,
        "age_half": 2,
        "phi_weight": 0.3,
        "weight_half": 0.5,
    }

    def __init__(self):
        self._age = 0

        expected_weight = self.params["w_birth"]
        std_weight = self.params["sigma_birth"]
        self._weight = (
            expected_weight + self.rng.standard_normal() * std_weight
        )

        self._recompute_fitness = True
        self._fitness = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._recompute_fitness = True
        self._age = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._recompute_fitness = True
        self._weight = value

    @property
    def fitness(self):
        if self.weight <= 0:
            return 0

        age_rate = self.params["phi_age"]
        age_half = self.params["age_half"]
        age_part = _sigmoid(age_rate * (self.age - age_half))

        weight_rate = self.params["phi_weight"]
        weight_half = self.params["weight_half"]
        weight_part = _sigmoid(-weight_rate * (self.weight - weight_half))

        return age_part * weight_part

    def should_move(self):
        return bool(self.rng.binomial(1, self.params["mu"] * self.fitness))

    def find_migration_destination(self, possible_cells):
        return possible_cells[0]

    def birth_season(self, current_cell):
        if self.weight < self.params["w_birth"] + self.params["sigma_birth"]:
            return False
        num_possible_mates = current_cell.get_animal_count(type(self)) - 1
        prob = min(1, self.params["gamma"] * self.fitness * num_possible_mates)
        if self.rng.binomial(1, 1 - prob):
            return

        baby = type(self)()
        weight_loss = self.params["zeta"] * baby.weight

        if weight_loss > self.weight:
            return

        self.weight -= weight_loss
        return baby

    def should_die(self):
        death_prob = self.params["omega"] * (1 - self.fitness)
        return self.fitness < 0 or self.rng.binomial(1, death_prob)
