import random
import string
from animal import Animals
from cell import Cell
from collections import OrderedDict
from operator import itemgetter

class World:
    def __init__(self, size):
        ''' [size]: (height, width) '''
        self.size = size
        self.cells = [[None for x in range(size[1])] for x in range(size[0])]
        self.rows = size[0]
        self.cols = size[1]
        self.current = 0
        self.high = size[1]
        self.steps = 0
        self.animals = set()
        self.species_count = {A: 0 for A in Animals.animals}
        self.counts = []

    def __iter__(self):
        return self

    def get_counts(self):
        c = self.species_count
        a = Animals.animals

        c[a[0]] = 0
        c[a[1]] = 0
        c[a[2]] = 0
        for animal in self.animals:
            if not animal.dead():
                c[type(animal)] += 1

        return (c[a[0]],c[a[1]],c[a[2]])

    def step(self):
        ''' do one time step in the world '''
        self.counts.append((self.get_counts()))
        for row in self.cells:
            for cell in row:
                cell.step()
        self.steps += 1


    def get_relative_cell(self, cell, d_row, d_col):
        new_row = cell.row + d_row
        new_col = cell.col + d_col
        def adjust(dim, max_dim):
            if dim < 0:
                return 0
            elif dim >= max_dim:
                return max_dim - 1
            return dim
        new_row = adjust(new_row, self.rows)
        new_col = adjust(new_col, self.cols)
        return self.cells[new_row][new_col]

    def randomly_populate_cells(self):
        for row, i in zip(self.cells, xrange(len(self.cells))):
            for j in range(len(row)):
                row[j] = Cell.random_cell(self, (row, j))

    def populate_cells(self):
        f_world = open('world_config/world.txt', 'r')
        world = f_world.read().split()
        f_world.close()
        f_anim = open('world_config/animals.txt', 'r')
        anim = f_anim.read().split()
        f_anim.close()
        i = 0
        for row, row_i in zip(self.cells, xrange(len(self.cells))):
            for j in range(len(row)):
                animal_i = int(anim[i])
                cell_animals = []
                if animal_i != 0:
                    animal = Animals.animals[animal_i-1](self)
                    cell_animals.append(animal)
                    self.species_count[type(animal)] += 1
                row[j] = Cell.from_int(int(world[i]), cell_animals, self, (row_i, j))
                self.animals.update(cell_animals)
                i += 1

    def next(self):
        if self.current >= self.high:
            self.current = 0
            raise StopIteration
        self.current += 1
        return self.cells[self.current-1]

    def set_cell(self, x, y, cell):
        cell.x = x
        cell.y = y
        self.cells[x][y] = cell

    def get_cell(self, x, y):
        return self.cells[x][y]

    def roulette(self, sorted_fitness, dic):
      r = random.randint(0, tot_fitness)
      S = 0
      i = 0
      while S < r:
        S += sorted_fitness[i]
        i += 1
      return dic[i-1]

    def reproduce(self):
      dic = {}
      tot_fitness = 0
      for animal in self.animals:
        fitness = animal.f_fitness()
        tot_fitness += fitness
        d[fitness] = animal

      if len(d) < 2:
        return

      sorted_fitness = sorted(dic.keys())

      animal1 = self.roulette(sorted_fitness, dic)
      animal2 = self.roulette(sorted_fitness, dic)
      while animal2 == animal1:
        self.roulette(sorted_fitness, dic)

      # we have selected two inidividuals to reproduce

      # crossover

      # mutation

    def print_animal_stats(self):
        #ret = 'Animal, Steps survived, Death cause'
        ret = ''
        for anim in self.animals:
            ret += '\n{} {} {}'.format(anim.get_name(), anim.last_step, anim.death_cause)

        with open('data/temp.txt', 'w') as f:
            f.write(ret)

        ret = ' '.join([a.__name__ for a in Animals.animals])
        for (a,b,c) in self.counts:
            ret += '\n{} {} {}'.format(a,b,c)
        with open('data/temp_timeseries.txt', 'w') as f:
            f.write(ret)

    def all_dead(self):
        for anim in self.animals:
            if not anim.dead():
                return False
        return True
