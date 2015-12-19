import random, math
from actions import *
from resources import Resources as R
from constance import *
from PIL import Image
from cell import Cell

class Diet:
    herbivore = [R.grass, R.fruit, R.leaves]
    carnivore = [R.fish]

MAX_STAT = 127
STAT_INC = 10
MATE_AGE = 150

class DeathCause:
    eaten = 'Eaten'
    thirst = 'Thirst'
    hunger = 'Hunger'

class Goal:
    explore, \
    eat,     \
    drink,   \
    mate,    \
    rest     = range(5)

class Animal(object):
    n_animals = 0

    def __init__(self, world, diet):
        self.world = world
        self.diet = diet
        self.prey = []
        self.color = 'Black'
        self.uid = Animal.n_animals
        Animal.n_animals += 1
        self.last_step = -1         # keeps track, so as not to move an animal
                                    # twice in one time step
        self.born_on = world.steps

        self.hunger = 0             # hunger level
        self.energy = MAX_STAT      # energy level
        self.thirst = 0             # thirst level

        self.last_eat = 0
        self.last_drink = 0
        self.last_sleep = 0

        self.is_dead = False
        self.death_cause = ''
        self.current_cell = None   # the cell the animal is currently in
        height = world.size[0]
        width = world.size[1]
        self.cells = [[None for x in range(width)] for x in range(height)]

        # this function is the AI part of Animal
        self.determine_action = self.random_determine_action

        self.thresh_scale = 6                 # 2^127 - 1 = 127
        # PARAMETERS
        self.hunger_thresh = 50                # 1 to 127 scale
        self.thirst_thresh = 50                # 1 to 127 scale
        self.energy_thresh = 50                # 1 to 127 scale
        self.mate_chance   = 0.01

    # convert an integer to its string binary representation
    @staticmethod
    def to_binary(val):
      n = int(math.log(val, 2))
      s = ''
      while val > 0:
        p = int(math.pow(2, n))
        if val >= p:
          s += '1'
          val -= p
        else:
          s += '0'
        n -= 1
      for x in xrange(n + 1):
        s += '0'
      return s

    # pad val with zeros so that it has length p
    @staticmethod
    def pad(val, p):
      while len(val) < p:
        val = '0' + val
      return val

    @staticmethod
    def pad_binary(val, threshold_scale):
      return Animal.pad(Animal.to_binary(val), threshold_scale)

    # convert an animal to its string binary representation
    # hunger_thresh :: thirst_thresh :: energy_thresh
    @staticmethod
    def to_string_rep(animal):
      ts = animal.thresh_scale
      rep_animal = Animal.pad_binary(animal.hunger_thresh, ts)
      rep_animal += Animal.pad_binary(animal.thirst_thresh, ts)
      rep_animal += Animal.pad_binary(animal.energy_thresh, ts)
      return rep_animal

    # crossover the strings rep1 and rep2 at a random index
    @staticmethod
    def crossover(rep1, rep2):
      n = len(rep1)
      c = random.randint(0, n)
      left1 = rep1[0:c]
      left2 = rep2[0:c]
      right1 = rep1[c:n]
      right2 = rep2[c:n]
      return left1 + right2, left2 + right1

    @staticmethod
    def negate(c):
      if c == '1':
        return '0'
      else:
        return '1'

    @staticmethod
    def mutate(rep):
      new_rep = ''
      for x in xrange(0,len(rep)):
        # mutate with probability 1/100
        r = random.randint(1, 100)
        if r == 1:    # mutate
          new_rep += Animal.negate(rep[x])
        else:         # don't mutate
          new_rep += rep[x]
      return new_rep

    # convert a binary string into an integer
    @staticmethod
    def to_int(s):
      n = 0
      i = 0
      x = len(s) - 1    # least siginificant digit
      while x >= 0:
        if s[x] == '1':
          i += math.pow(2, n)
        x -= 1
        n += 1
      return int(i)

    # generate a new animal by crossing over and mutation parent1 and parent2
    @staticmethod
    def birth_animal(parent1, parent2):
        assert parent1.world == parent2.world
        assert parent1.diet == parent2.diet
        assert parent1.__class__ == parent2.__class__

        print 'new animal born!'

        rep_parent1 = Animal.to_string_rep(parent1)
        rep_parent2 = Animal.to_string_rep(parent2)
        child1, child2 = Animal.crossover(rep_parent1, rep_parent2)
        r = random.randint(0,1)
        child = None
        if r == 0:
          child = Animal.mutate(child1)
        else:
          child = Animal.mutate(child2)

        Species = parent1.__class__
        baby = Species(parent1.world)

        ts = baby.thresh_scale
        baby.hunger_thresh = Animal.to_int(child[0:ts])
        baby.thirst_thresh = Animal.to_int(child[ts:2*ts])
        baby.energy_thresh = Animal.to_int(child[2*ts:3*ts])
        if parent1.get_name() == 'Tiger':
          baby.mate_chance = random.randint(0,5)/100
        else:
          baby.mate_chance = random.randint(0,10)/100
        return baby

    def eat(self):
        self.gain_thirst()
        self.last_eat = 0
        if self.hunger < STAT_INC:
            self.hunger = 0
        else:
            self.hunger -= STAT_INC

    def mate(self):
        self.gain_thirst()
        self.gain_hunger()
        self.lose_energy

    def gain_hunger(self):
        self.last_eat += 1
        if self.last_eat % 10 == 0:
            self.hunger += self.last_eat / 10
            self.hunger = min(MAX_STAT, self.hunger)

    def drink(self):
        self.gain_hunger()
        self.last_drink = 0
        if self.thirst < STAT_INC:
            self.thirst = 0
        else:
            self.thirst -= STAT_INC

    def gain_thirst(self):
        self.last_drink += 1
        if self.last_drink % 10 == 0:
            self.thirst += self.last_drink / 10
            self.thirst = min(MAX_STAT, self.thirst)

    def sleep(self):
        self.gain_hunger()
        self.gain_thirst()
        self.last_sleep = 0
        if self.energy > MAX_STAT - STAT_INC:
            self.energy = MAX_STAT
        else:
            self.energy += STAT_INC

    def lose_energy(self):
        self.last_sleep += 1
        if self.last_sleep % 10 == 0:
            self.energy -= self.last_sleep / 10
            self.energy = max(0, self.energy)

    def move(self):
        self.gain_hunger()
        self.gain_thirst()
        self.lose_energy()

    def get_name(self):
        return type(self).__name__

    def dead(self):
        return self.is_dead

    def death_cause(self):
        assert self.dead()
        return self.death_cause

    def __repr__(self):
        return '{}, hunger: {} ({}), thirst: {} ({}), energy: {} ({})'.format(
                self.get_name(), self.hunger, self.last_eat,
                                 self.thirst, self.last_drink,
                                 self.energy, self.last_sleep)

    def get_eat_action(self):
        ''' tries to find food to eat, otherwise returns None '''
        action = Eat()
        for food in self.diet:
            if self.current_cell.contains_resource(food):
                action.food = food

        for prey in self.prey:
            a = self.current_cell.get_animal_by_type(prey)
            if a is not None:
                action.food = a
                action.is_animal = True

        if action.food == None:
            return None
        return action

    def get_drink_action(self):
        ''' tries to find water, otherwise returns None '''
        if self.current_cell.contains_resource(R.water):
            return Drink()
        return None

    def random_determine_action(self):
        action = Actions.random_action()

        if type(action) == Eat:
            action = self.get_eat_action()
            if action == None:
                action = Sleep()

        return action

    def be_eaten(self):
        self.is_dead = True
        self.death_cause = DeathCause.eaten

    def naive_determine_action(self):
        action = None
        if self.thirst > 1:
            if self.hunger > self.thirst:
                action = self.get_eat_action()
            if action is None:
                action = self.get_drink_action()
        elif self.hunger > 1:
            action = self.get_eat_action()

        if action is None:
            action = Move(Direction.random_direction())

        return action

    def age(self):
        return self.world.steps - self.born_on

    def can_mate(self):
        return self.age() >= MATE_AGE

    def determine_goal(self):
        # Determines which goal to achieve, parameterized by its own need
        # thresholds.
        if self.thirst >= self.thirst_thresh and self.hunger >= self.hunger_thresh:
            if self.hunger > self.thirst:
                return Goal.eat
            else:
                return Goal.drink
        elif self.hunger >= self.hunger_thresh:
            return Goal.eat
        elif self.thirst >= self.thirst_thresh:
            return Goal.drink
        elif self.energy <= self.energy_thresh:
            return Goal.rest

        if self.can_mate():
            if random.random() < self.mate_chance:
                return Goal.mate

        return Goal.explore

    def explore_action(self):
        for neighbor in self.current_cell.get_neighbors():
            row,col = neighbor.row, neighbor.col

            if self.cells[row][col] is None:
                dir_to = Cell.direction_to(self.current_cell, neighbor)
                if dir_to is not None:
                    return Move(dir_to)

        oldest_cell = None
        oldest_time = 0
        for row, i in zip(self.cells, range(len(self.cells))):
            for cell, j in zip(row, range(len(row))):
                if cell is None:
                    dir_to = Cell.direction_to(self.current_cell, self.world.cells[i][j])
                    if dir_to is not None:
                        return Move(dir_to)
                else:
                    cell.step_time
                    if cell.step_time > oldest_time:
                        oldest_time = cell.step_time
                        oldest_cell = cell

        if oldest_cell is not None:
            dir_to = Cell.direction_to(self.current_cell, oldest_cell)
            if dir_to is not None:
                return Move(dir_to)

        return Move(Direction.random_direction())

    def find_closest(self, goal_func):
        # returns the nearest cell to self.current_cell that satisfies
        # (goal_func: CellSnapshot -> bool)
        satisfying_cells = {}         # map from cell to distance
        for row in self.cells:
            for cell_snapshot in row:
                if cell_snapshot is not None and goal_func(cell_snapshot):
                    dist = Cell.distance(self.current_cell, cell_snapshot)
                    satisfying_cells[cell_snapshot] = dist

        if len(satisfying_cells) == 0:
            return None

        best_cell, _ = min(satisfying_cells.iteritems(), key=lambda x: x[1])
        return best_cell

    def eat_action(self):
        local_food = self.get_eat_action()
        if local_food is not None:
            return local_food

        best_cell = self.find_closest(lambda cs: cs.has_food(self.diet + self.prey))
        if best_cell is not None:
            dir_to = Cell.direction_to(self.current_cell, best_cell)
            if dir_to is None:
                eat = self.get_eat_action()
                if eat is None:
                    return self.explore_action()
                else:
                    return eat

        return self.explore_action()

    def drink_action(self):
        local_drink = self.get_drink_action()
        if local_drink is not None:
            return local_drink
        else:
            best_cell = self.find_closest(lambda cs: cs.has_water())
            if best_cell is not None:
                dir_to = Cell.direction_to(self.current_cell, best_cell)
                if dir_to is not None:
                    return Move(dir_to)

        return self.explore_action()

    def mate_action(self):
        for animal in self.current_cell.animals:
            if animal == self:
                continue
            if type(animal) == type(self) and animal.can_mate():
                return Mate(animal)

        return self.explore_action()

    def determine_action_by_goal(self):
        goal = self.determine_goal()

        if goal == Goal.explore:
            #print 'goal: explore'
            return self.explore_action()
        elif goal == Goal.eat:
            #print 'goal: eat'
            return self.eat_action()
        elif goal == Goal.drink:
            #print 'goal: drink'
            return self.drink_action()
        elif goal == Goal.mate:
            #print 'goal: mate'
            return self.mate_action()
        else: # goal == rest
            #print 'goal: sleep'
            return Sleep()

    def update_state(self):
        if not self.is_dead:
            if self.thirst == MAX_STAT:
                self.is_dead = True
                self.death_cause = DeathCause.thirst
            elif self.hunger == MAX_STAT:
                self.is_dead = True
                self.death_cause = DeathCause.hunger

    def do_action(self, action):
        if type(action) == Eat:
            self.eat()

        elif type(action) == Drink:
            self.drink()

        elif type(action) == Move:
            self.move()

        elif type(action) == Mate:
            self.mate()

        else:
            assert type(action) == Sleep
            self.sleep()

    def act(self):
        action = self.determine_action()

        if not self.current_cell.can_perform_action(action):
            action = Sleep()
        if type(action) is Move and self.energy == 0:
            action = Sleep()

        self.do_action(action)
        self.update_state()
        return action

elephant = Image.open('elephant.png')
elephant1 = elephant.resize((CELL_PIXELS, CELL_PIXELS),Image.ANTIALIAS)
elephant2 = elephant.resize((CELL_PIXELS/2, CELL_PIXELS),Image.ANTIALIAS)
elephant3 = elephant.resize((CELL_PIXELS/3, CELL_PIXELS),Image.ANTIALIAS)

tiger = Image.open('tiger.png')
tiger1 = tiger.resize((CELL_PIXELS, CELL_PIXELS),Image.ANTIALIAS)
tiger2 = tiger.resize((CELL_PIXELS/2, CELL_PIXELS),Image.ANTIALIAS)
tiger3 = tiger.resize((CELL_PIXELS/3, CELL_PIXELS),Image.ANTIALIAS)

giraffe = Image.open('giraffe.png')
giraffe1 = giraffe.resize((CELL_PIXELS, CELL_PIXELS),Image.ANTIALIAS)
giraffe2 = giraffe.resize((CELL_PIXELS/2, CELL_PIXELS),Image.ANTIALIAS)
giraffe3 = giraffe.resize((CELL_PIXELS/3, CELL_PIXELS),Image.ANTIALIAS)

class AnimalPhotos:
    giraffe = [giraffe1, giraffe2, giraffe3]
    tiger = [tiger1, tiger2, tiger3]
    elephant = [elephant1, elephant2, elephant3]

class Elephant(Animal):
    def __init__(self, world):
        super(Elephant,self).__init__(world, Diet.herbivore)
        self.color = 'Purple'
        self.photo = elephant
        #self.determine_action = self.naive_determine_action
        self.determine_action = self.determine_action_by_goal

class Tiger(Animal):
    def __init__(self, world):
        super(Tiger,self).__init__(world, Diet.carnivore)
        self.prey = [Elephant, Giraffe]
        self.color = 'Orange'
        self.photo = tiger
        #self.determine_action = self.naive_determine_action
        self.determine_action = self.determine_action_by_goal

class Giraffe(Animal):
    def __init__(self, world):
        super(Giraffe,self).__init__(world, Diet.herbivore)
        self.color = 'Yellow'
        #self.determine_action = self.naive_determine_action
        self.determine_action = self.determine_action_by_goal

class Animals:
    animals = [Giraffe, Elephant, Tiger]
