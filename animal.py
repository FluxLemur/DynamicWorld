import random
from actions import *
from resources import Resources as R
from constance import *
from PIL import Image

class Diet:
    herbivore = [R.grass, R.fruit, R.leaves]
    carnivore = [R.fish]

MAX_STAT = 11
STAT_INC = 2

class State:
    hungry,      \
    thirsty,     \
    tired,       \
    dead_hunger, \
    dead_thirst = range(5)

class Animal(object):
    n_animals = 0

    def __init__(self, world, diet):
        self.world = world
        self.diet = diet
        self.color = 'Black'
        self.uid = Animal.n_animals
        Animal.n_animals += 1

        self.conditions = set()     # empty set is healthy
        self.last_step = -1         # keeps track, so as not to move an animal
                                    # twice in one time step

        self.hunger = 0             # hunger level
        self.energy = MAX_STAT      # energy level
        self.thirst = 0             # thirst level

        self.last_eat = 0
        self.last_drink = 0
        self.last_sleep = 0

        self.is_dead = False
        self.attacks = 0                                                            # number of attacks the animal has been subject to
        self.current_cell = None                                                    # the cell the animal is currently in
        height = world.size[0]
        width = world.size[1]
        self.cells = [[None for x in range(width)] for x in range(height)]

        # this function is the AI part of Animal
        self.determine_action = self.random_determine_action

        # animal has some internal rep. of the world

    #def f_fitness(self):        # fitness function
    #    return self.energy - self.hunger - self.thirst - self.attacks * 2

    def eat(self):
        self.gain_thirst()
        self.last_eat = 0
        if self.hunger < STAT_INC:
            self.hunger = 0
        else:
            self.hunger -= STAT_INC

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
        if self.hunger == MAX_STAT and self.thirst == MAX_STAT:
            return 'Thirst and Hunger'
        elif self.hunger == MAX_STAT:
            return 'Hunger'
        else:
            return 'Thirst'

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

    def eat_score(self):
        action = self.get_eat_action()
        if action is None:
            return None, 0
        return action, 1

    def drink_score(self):
        action = self.get_drink_action()
        if action is None:
            return None, 0
        return action, 1

    def sleep_score(self):
        return Sleep(), 1

    def move_north_score(self):
        return Move(Direction.north), 1

    def move_south_score(self):
        return Move(Direction.south), 1

    def move_east_score(self):
        return Move(Direction.east), 1

    def move_west_score(self):
        return Move(Direction.west), 1

    def determine_action_by_score(self):
        actions = []  # should be of the form [(action obj, int score) ...]
                      # TODO: think about normalizing the scores somehow

        actions.append(self.eat_score())
        actions.append(self.drink_score())
        actions.append(self.sleep_score())
        actions.append(self.move_north_score())
        actions.append(self.move_south_score())
        actions.append(self.move_east_score())
        actions.append(self.move_west_score())

        actions.sort(key=lambda a: -a[1])

        return actions[0][0]

    def update_state(self):
          self.is_dead = self.hunger == MAX_STAT or self.thirst == MAX_STAT

    def do_action(self, action):
        if type(action) == Eat:
            self.eat()

        elif type(action) == Drink:
            self.drink()

        elif type(action) == Move:
            self.move()

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
elephant = elephant.resize((CELL_PIXELS/2, CELL_PIXELS/2),Image.ANTIALIAS)

tiger = Image.open('tiger.png')
tiger = tiger.resize((CELL_PIXELS/2, CELL_PIXELS/2),Image.ANTIALIAS)

giraffe = Image.open('giraffe.png')
giraffe = giraffe.resize((CELL_PIXELS/2, CELL_PIXELS/2),Image.ANTIALIAS)

class Elephant(Animal):
    def __init__(self, world):
        super(Elephant,self).__init__(world, Diet.herbivore)
        self.prey = []
        self.color = 'Purple'
        self.photo = elephant
        self.determine_action = self.naive_determine_action

class Tiger(Animal):
    def __init__(self, world):
        super(Tiger,self).__init__(world, Diet.carnivore)
        self.prey = [Elephant, Giraffe]
        self.color = 'Orange'
        self.photo = tiger

class Giraffe(Animal):
    def __init__(self, world):
        super(Giraffe,self).__init__(world, Diet.herbivore)
        self.prey = []
        self.color = 'Yellow'
        self.photo = giraffe
        self.determine_action = self.determine_action_by_score

class Animals:
    animals = [Giraffe, Elephant, Tiger]
