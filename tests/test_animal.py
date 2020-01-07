import biosim as animals


class TestAnimal:
    def test_correct_fit(self):
        animal = animals.Animal()
        animal.weight = 0.5
        animal.age = 2

        assert animal.fitness == 0.25
