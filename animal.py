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

class DeathCause:
    eaten = 'Eaten'
    thirst = 'Thirst'
    hunger = 'Hunger'

class Goal:
    explore,  \
    eat,      \
    drink,    \
    mate,     \
    sleep     = range(5)

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
        self.prey = []
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
        self.death_cause = ''
        self.current_cell = None   # the cell the animal is currently in
        height = world.size[0]
        width = world.size[1]
        self.cells = [[None for x in range(width)] for x in range(height)]

        # this function is the AI part of Animal
        self.determine_action = self.random_determine_action

    #def f_fitness(self):        # fitness function
    #    return self.energy - self.hunger - self.thirst - self.attacks * 2

    @staticmethod
    def birth_animal(parent1, parent2):
        # TODO: finish this
        assert parent1.world == parents2.world
        assert parent1.diet == parents2.diet

        return Animal(parent1.world, parent1.diet)

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

    def determine_goal(self):
        # TODO: how to pick goal?
        return Goal.explore

    def explore_action(self):
        # TODO: think about exploration heuristics
        return Move(Direction.random_direction())

    def eat_action(self):
        # TODO: find cell with food, and go towards there, or eat here
        pass

    def drink_action(self):
        # TODO: similar to eat
        pass

    def mate_action(self):
        # TODO: think about how this should be done
        pass

    def determine_action_by_goal(self):
        goal = self.determine_goal(self)

        if goal == Goal.explore:
            return self.explore_action()
        elif goal == Goal.eat:
            return self.eat_action()
        elif goal == Goal.drink:
            return self.drink_action()
        elif goal == Goal.mate:
            return self.mate_action()
        else: # goal == sleep
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
        self.determine_action = self.naive_determine_action

class Tiger(Animal):
    def __init__(self, world):
        super(Tiger,self).__init__(world, Diet.carnivore)
        self.prey = [Elephant, Giraffe]
        self.color = 'Orange'

class Giraffe(Animal):
    def __init__(self, world):
        super(Giraffe,self).__init__(world, Diet.herbivore)
        self.color = 'Yellow'
        self.determine_action = self.naive_determine_action

class Animals:
    animals = [Giraffe, Elephant, Tiger]