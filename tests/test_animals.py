
from biosim.animals import Herbivore


class TestAnimals:
    """
    Test class for animal properties
    """
    def test_fitness(self):
        """
        Test that the fitness is calculated properly
        :return:
        """
        pass

    def test_move(self):
        """
        Test that both animal types can move properly
        :return:
        """
        pass

    def test_mountain_and_water_impassable(self):
        """
        Test that animals cannot move through mountains or water
        :return:
        """
        pass

    def test_eating(self):
        """
        Test that eating works as it should
        :return:
        """
        pass

    def test_mating_and_weight(self):
        """
        Test the mating function, and that there is no offspring if offsprings
        weight surpasses the weight of the mother
        :return:
        """
        pass

    def test_death(self):
        """
        Test that an animal dies if its fitness is 0
        :return:
        """
        pass

    def test_hunting(self):
        """
        Test the hunting capabilities of the predators. Go for the herbivore
        with lowest fitness and stop if all herbivores have been attempted
        :return:
        """
        pass
