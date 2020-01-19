# -*- coding: utf-8 -*-


__author__ = "Sebastian Kihle & Andreas Hoeimyr"
__email__ = "sebaskih@nmbu.no & andrehoi@nmbu.no"

from biosim.animals import Herbivore, Carnivore
from biosim.island_class import Map
import textwrap
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import random
import subprocess


class BioSim:
    def __init__(
            self,
            island_map,
            ini_pop,
            seed,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt="png",
    ):
        """
        The BioSim class will simulate an ecosystem on an island. You need
        to input a string with the map geography and add animals such as
        herbivores and carnivores to simulate. The class will display an
        interface with a colored map of the island, a heatmap for the
        herbivores, a heatmap for the carnivores and population graph.
        This interface will be updated every year by default, but these
        parameters can be changed. You will also have the option to save
        frames(pictures) of the simulation, and be able to construct a video
        from them.

        :param island_map: Multi-line string specifying island geography.

        :param ini_pop: List of dictionaries specifying initial population.

        :param seed: Integer used as random number seed.

        :param ymax_animals: Number specifying y-axis limit for graph.
        Shows the population of each animal species. If ymax_animals is None,
        the y-axis limit is set to a fixed number, e.g., 8000.

        :param cmax_animals: Dictionary specifying color-code limits.
        If cmax_animals is None, sensible, fixed default values should be
        used. cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}

        :param img_base: String with beginning of file name for figures.
        Must include path. If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name

        :param img_fmt: String with file type for figures, e.g. 'png'
        """

        self.map = Map(island_map)
        self.island_map = island_map
        self.seed = random.seed(seed)
        self.current_year = 0
        self.sim_year = 0

        # The following will be initialized by _setup_graphics.
        self._fig = None
        self._heatmap_herb_ax = None
        self._heatmap_herb_graphics = None
        self._line_graph_ax = None
        self.line_graph = None
        self.legend_is_set_up = False

        self.add_population(ini_pop)

        self._img_base = img_base
        self._img_fmt = img_fmt
        self._img_counter = 0

        if ymax_animals is None:
            self.graph_ymax = 8000
        else:
            self.graph_ymax = ymax_animals

        if cmax_animals is None:
            self.color_bar_max_herb = 150
            self.color_bar_max_carn = 100
        else:
            self.color_bar_max_herb = cmax_animals['Herbivore']
            self.color_bar_max_carn = cmax_animals['Carnivore']

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species.
        :param params: Dictionary with parameter specification for species.
        """

        class_dict = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        class_dict[species].new_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for biome type.

        :param landscape: String, code letter for biome.
        :param params: Dictionary with valid parameter specification for biome.
        """
        self.map.biome_dict[landscape].biome_parameters(params)

    def feeding_cycle(self, prints=False):
        """
        Eating cycle for each animal in each cell. The animal with the
        highest fitness eats first for each species. The carnivores will try to
        eat the herbivores with the lowest fitness first.

        :param prints: Prints relevant actions if True.
        """

        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'Feeding')

            cell.regrow()

            # Sorts each list in according to order of descending fitness.
            cell.present_herbivores.sort(key=lambda x: x.phi, reverse=True)
            cell.present_carnivores.sort(key=lambda x: x.phi, reverse=True)

            # Eating method for the herbivores.
            for herbivore in cell.present_herbivores:
                cell.available_food = herbivore.eat(cell.available_food)
                if prints:
                    print('Weight of herbivore:', herbivore.weight)

            cell.present_herbivores.sort(key=lambda x: x.phi)
            # Eating method for each carnivore in cell.
            for carnivore in cell.present_carnivores:
                carnivore.hunt(cell.present_herbivores)

                # Only keeps the herbivores that survived the hunt
                alive_herbivores = [herbivore for herbivore in
                                    cell.present_herbivores if herbivore.alive]

                cell.present_herbivores = alive_herbivores

    def breeding_cycle(self, prints=False):
        """
        Method for yearly breeding for all animals. All animals breed.
        Animals have no gender, so there only needs to be one other animal
        of same species in the cell to reproduce. The weight of the newborn
        is drawn from a Gaussian distribution, and the mother loses the
        weight of the newborn.

        :param prints: Prints relevant actions if True.
        """

        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'Breeding')

            # Creates new list so that newborns dont breed.
            current_herbivores = cell.present_herbivores
            newborn_herbivores = []
            for herbivore in cell.present_herbivores:
                # Checks if there is born a new animal, and potentially
                # adds it to a list of newborn animals in the cell.
                new_herbivore = herbivore.breeding(len(
                    current_herbivores))
                if new_herbivore is not None:
                    newborn_herbivores.append(new_herbivore)

            # Updates the herbivores present in the cell.
            cell.present_herbivores = current_herbivores + newborn_herbivores

            # Creates new list so that newborns dont breed.
            current_carnivores = cell.present_carnivores
            newborn_carnivores = []
            for carnivore in cell.present_carnivores:
                # Checks if there is born a new animal, and potentially
                # adds it to a list of newborn animals in the cell.
                new_carnivore = carnivore.breeding((len(
                    current_carnivores)))
                if new_carnivore is not None:
                    newborn_carnivores.append(new_carnivore)

            # Updates the carnivores present in the cell.
            cell.present_carnivores = current_carnivores + newborn_carnivores

    def migration_cycle(self, prints=False):
        """
        Migration method that moves all animals on the map. Animals have a
        parameter that tracks if the animal has moved during the year. This
        is to keep animals from moving twice. Animals move depending on
        fitness, where the animal of each species with the highest fitness
        moves first.

        :param prints: Prints relevant actions if True.
        """

        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'migration')

            # Sorts each list in according to order of descending fitness.
            cell.present_herbivores.sort(key=lambda x: x.phi, reverse=True)
            cell.present_carnivores.sort(key=lambda x: x.phi, reverse=True)

            # Herbivores in cell at start of cycle.
            migrating_herbivores = cell.present_herbivores

            # Herbivores that leave the current cell.
            exited_herbivores = []

            for herbivore in migrating_herbivores:
                if not herbivore.has_moved:
                    target_cell = herbivore.migrate(self.map.top,
                                                    self.map.bottom,
                                                    self.map.left,
                                                    self.map.right)
                    herbivore.has_moved = True

                    # Moves to the target cell unless it is an invalid biome.
                    if target_cell is not None:
                        target_cell.present_herbivores.append(herbivore)
                        exited_herbivores.append(herbivore)
                        if prints:
                            print('An animal moved to ',
                                  type(target_cell).__name__)

            # Updates present herbivores in the cell.
            cell.present_herbivores = [animal for animal in
                                       migrating_herbivores if animal not in
                                       exited_herbivores]

            # Carnivores in cell at start of cycle.
            migrating_carnivores = cell.present_carnivores

            # Carnivores that leave the current cell.
            exited_carnivores = []

            for carnivore in migrating_carnivores:
                if not carnivore.has_moved:
                    target_cell = carnivore.migrate(self.map.top,
                                                    self.map.bottom,
                                                    self.map.left,
                                                    self.map.right)
                    carnivore.has_moved = True

                    # Moves to target cell unless its an invalid biome.
                    if target_cell is not None:
                        target_cell.present_carnivores.append(carnivore)
                        exited_carnivores.append(carnivore)
                        if prints:
                            print('An animal moved to ',
                                  type(target_cell).__name__)

            # Updates the present carnivores in current cell.
            cell.present_carnivores = [animal for animal in
                                       migrating_carnivores if animal not in
                                       exited_carnivores]

    def ageing_cycle(self, prints=False):
        """
        Ages all animals on the map by one year.

        :param prints: Prints relevant actions if True.
        """

        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'ageing')

            # Ages the herbivores, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.ageing()
                if prints:
                    print('Age:', herbivore.age)

            for carnivore in cell.present_carnivores:
                carnivore.ageing()
                if prints:
                    print('Age:', carnivore.age)

    def weight_loss_cycle(self, prints=False):
        """
        Each animal on the map loses weight.

        :param prints: Prints relevant actions if True.
        """
        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'weight_loss')

            # The herbivores lose weight, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.lose_weight()
                if prints:
                    print('Weight after loss:', herbivore.weight)

            for carnivore in cell.present_carnivores:
                carnivore.lose_weight()
                if prints:
                    print('Weight after loss:', carnivore.weight)

    def death_cycle(self, prints=False):
        """
        Each animal has a chance of dying. Probability is depending on the
        fitness. The lowers the fitness, the higher the chances of dying.
        Removes dead animals.

        :param prints: Prints relevant actions if True.
        """

        for cell in self.map.map_iterator():
            if prints:
                print('Current cell:', type(cell).__name__, 'death')

            # Checks if the herbivores dies, then the carnivores.
            for herbivore in cell.present_herbivores:
                herbivore.potential_death()

            for carnivore in cell.present_carnivores:
                carnivore.potential_death()

            # Removes animals killed from natural causes.
            alive_herbivores = [herbivore for herbivore in
                                cell.present_herbivores if herbivore.alive]

            dead = len(cell.present_herbivores) - len(alive_herbivores)

            if dead > 0:
                if prints:
                    print(dead, 'Herbivores died')

            # Updates living herbivores in cell.
            cell.present_herbivores = alive_herbivores

            alive_carnivores = [carnivore for carnivore in
                                cell.present_carnivores if carnivore.alive]

            dead = len(cell.present_carnivores) - len(alive_carnivores)

            if dead > 0:
                if prints:
                    print(dead, 'Carnivores died')

            # Updates living carnivores in cell.
            cell.present_carnivores = alive_carnivores

    def simulate(self, num_years, vis_years=1, img_years=None, prints=False):
        """
        Run simulation while visualizing the result. Each year consists of
        going through the feeding cycle of all animals, then the breeding
        cycle for all animals, then migration cycle, aging cycle weight loss
        cycle and lastly the death cycle. Visualization will happen at the
        end of each year, along with the resetting of the has_moved parameter.
        The simulation will run until it has reached the desired number of
        years simulated. The simulation also tracks the amount of years that
        have been simulated.

        :param num_years: number of years to simulate.
        :param vis_years: years between visualization updates.
        :param img_years: years between visualizations saved to files.
        :param prints: Option to print the actions in each cell.

        Image files will be numbered consecutively.
        """
        self.sim_year = 0

        self._setup_graphics(num_years)
        while True:

            # Yearly actions for all animals.
            self.feeding_cycle(prints)
            self.breeding_cycle(prints)
            self.migration_cycle(prints)
            self.ageing_cycle(prints)
            self.weight_loss_cycle(prints)
            self.death_cycle(prints)

            # Makes all animals able to move again next year.
            for cell in self.map.map_iterator():
                for herbivore in cell.present_herbivores:
                    herbivore.has_moved = False

                for carnivore in cell.present_carnivores:
                    carnivore.has_moved = False

            if self.current_year % vis_years == 0:
                self._update_graphics()

            if img_years is not None:
                if self.current_year % img_years == 0:
                    self._save_graphics()

            self.sim_year += 1
            self.current_year += 1
            if prints:
                print('Current year in sim:', self.sim_year)

            if self.sim_year >= num_years:
                self._update_graphics()
                return

    def add_population(self, population):
        """
        Add a population to the island.

        :param population: List of dictionaries specifying population and place
        E. g.
        [{'loc': (y, x),
        'pop': [{'species': 'Herbivore', 'age': 1, 'weight': 15},
        {'species': 'Carnivore', 'age': 1, 'weight': 15}]
        }]
        """
        # Unpacks the coordinates and animals to add.
        # Adds new animals to a temporary list.
        for dictionary in population:
            coordinates = dictionary['loc']
            animals_to_add = []

            # Gets each new animal
            for element in dictionary['pop']:
                animals_to_add.append(element)

            # Unpacks the species value, and creates new class instance of
            # class type corresponding to species.
            # New class instance uses age and weight values from dictionary.
            for animal in animals_to_add:
                if animal['age'] < 0 or animal['weight'] < 0:
                    raise ValueError('Age and weight cannot be negative')

                animal_class = animal['species']

                if animal_class == 'Herbivore':
                    new_animal = Herbivore(animal['age'], animal['weight'])

                    if type(self.map.array_map[coordinates]).__name__ not in \
                            new_animal.legal_biomes:
                        raise ValueError('This animal cannot be placed in '
                                         'this biome')
                    self.map.array_map[coordinates]. \
                        present_herbivores.append(new_animal)

                if animal_class == 'Carnivore':
                    new_animal = Carnivore(animal['age'], animal['weight'])
                    if type(self.map.array_map[coordinates]).__name__ not in \
                            new_animal.legal_biomes:
                        raise ValueError('This animal cannot be placed in '
                                         'this biome')
                    self.map.array_map[coordinates]. \
                        present_carnivores.append(new_animal)

    @property
    def year(self):
        """
        Property that returns the current year.
        :return: Last year simulated.
        """""
        return self.current_year

    @property
    def num_animals(self):
        """
        Counts the total number of all animals on the island.
        :return: Total number of animals on island.
        """
        animal_counter = 0

        for cell in self.map.map_iterator():
            for _ in cell.present_herbivores:
                animal_counter += 1

            for _ in cell.present_carnivores:
                animal_counter += 1
        return animal_counter

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.

        :return: Dictionary with number of animals per species.
        """
        animal_dictionary = {}
        herbivore_counter = 0
        carnivore_counter = 0

        # Counts all animals in all cells
        for cell in self.map.map_iterator():
            for herbivore in cell.present_herbivores:
                herbivore_counter += 1

            for carnivore in cell.present_carnivores:
                carnivore_counter += 1

        animal_dictionary['Herbivore'] = herbivore_counter
        animal_dictionary['Carnivore'] = carnivore_counter

        return animal_dictionary

    @property
    def animal_distribution(self):
        """
        Creates a Pandas DataFrame with animal count per species for
        each cell on island.
        :return: Pandas DataFrame with animal distribution.
        """
        list_of_all_herbivores = []
        list_of_all_carnivores = []
        list_of_rows = []
        list_of_columns = []
        for cell in self.map.map_iterator():
            list_of_all_herbivores.append(len(cell.present_herbivores))
            list_of_all_carnivores.append(len(cell.present_carnivores))
            list_of_rows.append(self.map.y)
            list_of_columns.append(self.map.x)

        distribution_dict = {'Herbivore': list_of_all_herbivores,
                             'Carnivore': list_of_all_carnivores,
                             'Row': list_of_rows, 'Col': list_of_columns}
        data_frame = pd.DataFrame(distribution_dict, columns=['Row',
                                                              'Col',
                                                              'Carnivore',
                                                              'Herbivore'])
        return data_frame

    @property
    def herb_array(self):
        """
        Creates an array of the distribution of herbivores on the island.
        This is used to create the heatmaps.
        :return: A Numpy array with population of herbivores in each cell.
        """
        x_length = len(self.map.array_map[0])
        y_length = len(self.map.array_map.T[0])

        herb_array = np.zeros((y_length, x_length))

        for cell in self.map.map_iterator():
            herb_array[self.map.y, self.map.x] = len(cell.present_herbivores)
        return herb_array

    @property
    def carn_array(self):
        """
        Creates an array of the distribution of carnivores on the island.
        This is used to create the heatmap for carnivores.
        :return: A Numpy array with population of herbivores in each cell.
        """
        x_length = len(self.map.array_map[0])
        y_length = len(self.map.array_map.T[0])

        carn_array = np.zeros((y_length, x_length))

        for cell in self.map.map_iterator():
            carn_array[self.map.y, self.map.x] = len(cell.present_carnivores)
        return carn_array

    def _create_colour_island(self, map):
        """
        Creates a colored map of the island.
        :param map: The string map
        :return:
        """
        self.rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                          'M': (0.5, 0.5, 0.5),  # grey
                          'J': (0.0, 0.6, 0.0),  # dark green
                          'S': (0.5, 1.0, 0.5),  # light green
                          'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[self.rgb_value[column] for column in row] for row in
                   map.splitlines()]

        self._landscape_map_ax.imshow(map_rgb)
        self._landscape_map_ax.grid(True)
        self._landscape_map_ax.set_xticks(range(len(map_rgb[0])))
        self._landscape_map_ax.set_xticklabels(range(len(map_rgb[0])))
        self._landscape_map_ax.set_yticks(range(len(map_rgb)))
        self._landscape_map_ax.set_yticklabels(range(len(map_rgb)))

    def _setup_graphics(self, num_years):
        """
        Creates a interface with 4 subplots. A map of the island with
        colors, two heatmaps, one line graph and a colored map of the island.
        Each heatmap depicts the distribution of an animal, one for
        herbivores and one for carnivores. The line graph shows the total
        number of each animal species on the island each year. The colored map
        shows the position of the biomes on the map.

        :param num_years: Number of years simulated.
        """

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()
            self._fig.subplots_adjust(hspace=0.75)
            self._fig.suptitle('Model of the Ecosystem of Rossoya')

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._heatmap_herb_ax is None:
            self._heatmap_herb_ax = self._fig.add_subplot(3, 2, 3)
            self._heatmap_herb_graphics = None

            self._heatmap_carn_ax = self._fig.add_subplot(3, 2, 5)
            self._heatmap_carn_graphics = None

            self._landscape_map_ax = self._fig.add_subplot(3, 2, 1)

            self._create_colour_island(self.island_map)

            # Create the legend for the graphics
            if not self.legend_is_set_up:
                axlg = self._fig.add_axes([0.02, 0.72, 0.08, 0.15])
                axlg.axis('off')
                for ix, name in enumerate(('Ocn', 'Mtn', 'Jgl',
                                           'Svn', 'Dst')):
                    axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                                 edgecolor='none',
                                                 facecolor=self.rgb_value[name[
                                                     0]]))
                    axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

                self._landscape_map_ax.title.set_text('Island map')
                self._heatmap_herb_ax.title.set_text('Herbivore heatmap')
                self._heatmap_carn_ax.title.set_text('Carnivore heatmap')
                self._landscape_map_ax.get_xaxis().set_visible(False)
                self._landscape_map_ax.get_yaxis().set_visible(False)
                self._heatmap_herb_ax.get_xaxis().set_visible(False)
                self._heatmap_herb_ax.get_yaxis().set_visible(False)
                self._heatmap_carn_ax.get_xaxis().set_visible(False)
                self._heatmap_carn_ax.get_yaxis().set_visible(False)

        # Add right subplot for line graph of mean.
        if self._line_graph_ax is None:
            self._line_graph_ax = self._fig.add_subplot(1, 2, 2)
            self._line_graph_ax.set_ylim(0, self.graph_ymax)

        # needs updating on subsequent calls to simulate()
        self._line_graph_ax.set_xlim(0, num_years + self.current_year)

        if self.line_graph is None:
            herbivores_per_year = self._line_graph_ax.plot(

                np.arange(0, num_years + self.current_year + 1),
                np.full(num_years + self.current_year + 1, np.nan), 'g',
                label='Herbivore count'

            )

            carnivores_per_year = self._line_graph_ax.plot(

                np.arange(0, num_years + self.current_year + 1),
                np.full(num_years + self.current_year + 1, np.nan), 'r',
                label='Carnivore count'

            )

            if not self.legend_is_set_up:
                self._line_graph_ax.legend(loc='upper left', mode='expand')
                self.legend_is_set_up = True

            self.herbivore_line_graph = herbivores_per_year[0]
            self.carnivore_line_graph = carnivores_per_year[0]
        else:
            years, herbivores = self.herbivore_line_graph.get_data()
            years, carnivores = self.carnivore_line_graph.get_data()

            new_year = np.arange(years[-1] + 1, num_years)
            if len(new_year) > 0:

                herbivore_new = np.full(new_year.shape, np.nan)
                self.herbivore_line_graph.set_data(
                    np.hstack((years, new_year)),
                    np.hstack((herbivores, herbivore_new))
                )

                carnivore_new = np.full(new_year.shape, np.nan)
                self.carnivore_line_graph.set_data(
                    np.hstack((years, new_year)),
                    np.hstack((carnivores, carnivore_new))
                )

    def _update_system_map_herbivore(self, animal_array):
        """
        Updates the heatmap for herbivore distribution.

        :param animal_array: array of the distribution of animals
        """

        if self._heatmap_herb_graphics is not None:
            self._heatmap_herb_graphics.set_data(animal_array)
        else:
            self._heatmap_herb_graphics = \
                self._heatmap_herb_ax.imshow(animal_array,
                                             interpolation='nearest',
                                             vmin=0,
                                             vmax=self.color_bar_max_herb)
            plt.colorbar(self._heatmap_herb_graphics, ax=self._heatmap_herb_ax,
                         orientation='horizontal')

    def _update_system_map_carnivore(self, animal_array):
        """
        Updates the heatmap for carnivore distribution.

        :param animal_array: array of the distribution of animals
        """

        if self._heatmap_carn_graphics is not None:
            self._heatmap_carn_graphics.set_data(animal_array)
        else:
            self._heatmap_carn_graphics = \
                self._heatmap_carn_ax.imshow(animal_array,
                                             interpolation='nearest',
                                             vmin=0,
                                             vmax=self.color_bar_max_carn,
                                             cmap='magma')
            plt.colorbar(self._heatmap_carn_graphics, ax=self._heatmap_carn_ax,
                         orientation='horizontal')

    def _update_num_animals_graph(self, num_herbivores, num_carnivores):
        """
        Updates the line graph with two lines. One for the number of
        herbivores on the island and one for the number of carnivores
        on the island.
        :param num_herbivores: Number of herbivores on island.
        :param num_carnivores: Number of carnivores on island.
        """
        ydata = self.herbivore_line_graph.get_ydata()
        ydata[self.year] = num_herbivores
        self.herbivore_line_graph.set_ydata(ydata)

        cdata = self.carnivore_line_graph.get_ydata()
        cdata[self.year] = num_carnivores
        self.carnivore_line_graph.set_ydata(cdata)

    def _update_graphics(self):
        """
        Updates all the subplots on the graphical interface with the new
        graphics from _update_num_animals_graph,
        _update_system_map_carnivore and _update_system_map_herbivore methods.
        """

        self._update_system_map_herbivore(self.herb_array)

        self._update_system_map_carnivore(self.carn_array)

        self._update_num_animals_graph(

            self.num_animals_per_species['Herbivore'],
            self.num_animals_per_species['Carnivore']

        )

        plt.pause(1e-6)

    def _save_graphics(self):
        """Saves graphics to file if file name given."""

        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_counter,
                                                     type=self._img_fmt))
        self._img_counter += 1

    def make_movie(self):
        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
        """
        _FFMPEG_BINARY = 'ffmpeg'
        movie_fmt = 'mp4'

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to
                # http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format
                                       (self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))

        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)


if __name__ == "__main__":
    geogr = """\
                   OOOOOOOOOOOOOOOOOOOOO
                   OOOOOOOOSMMMMJJJJJJJO
                   OSSSSSJJJJMMJJJDDJJOO
                   OSSSSSSSSSMMJJJDJJOOO
                   OSSSSSJJJJJJJJJJJJOOO
                   OOOOOOOOOOOOOOOOOOOOO"""

    easy_sim = """\
                   OOOOOO
                   OJJJJO
                   OOJJOO
                   OOJOOO
                   OOOOOO"""

    geogr = textwrap.dedent(geogr)
    easy_sim = textwrap.dedent(easy_sim)

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
    ], seed=3, img_base="/Users/Andreas/Documents/inf200_january/"
                        "biosim_G07_sebastian_andreas/images/k")

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
    print('added carnivores to simulation')
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

    k.simulate(50)
    print(k.num_animals)
    plt.show()

    """
    for map_cell in k.map.map_iterator():
        print(map_cell)
    """
    """
    k = BioSim(island_map=easy_sim, ini_pop=[
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0}]},
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0}
                 ]}
    ], seed=0)

    k.simulate(50)

    k.add_population([
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 {"species": "Carnivore", "age": 1, "weight": 35.0},
                 ]}])
    k.simulate(50)
    print(k.num_animals_per_species['Herbivore'])
    plt.show()
    """

    """
    k = BioSim(island_map=geogr, ini_pop=[
        {"loc": (3, 3),
         "pop": [{"species": "Herbivore", "age": 7, "weight": 15.0}]},
        {"loc": (4, 1),
         "pop": [{"species": "Herbivore", "age": 1, "weight": 15.0},
                 {"species": "Herbivore", "age": 1, "weight": 15.0}
                 ]}
    ], seed=0, img_base="/Users/sebastiankihle/Documents/Python/INF200"
                        "/biosim_G07_sebastian_andreas/biosim/src/biosim/img/k",
               ymax_animals=10, cmax_animals=5)

    k.simulate(10)

    print('added carnivores to simulation')
    k.add_population([
        {
            "loc": (4, 1),
            "pop": [
                {"species": "Carnivore", "age": 3, "weight": 45.0},
                {"species": "Carnivore", "age": 2, "weight": 17.0}
            ],
        },
    ])

    k.simulate(10)
    print(k.num_animals)
    k.simulate(10)
    plt.show()
    """