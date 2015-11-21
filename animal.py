import random
from actions import *

class Diet:
    herbivore = 0
    carnivore = 1
    omnivore  = 2

class Animal:
    def __init__(self, world, diet):
        self.world = world
        self.diet = diet
        self.hunger = 0

        # the cell the animal is currently in
        self.cell = None

        # eating, moving, resting ...
        self.state = None

        # animal has some internal rep. of the world

    def act(self):
        action_cons = Actions.random_action_cons()
        if action_cons == Eat:
            # eat something random in the cell
            return Eat(None)
        else:
            return action_cons()

class Elephant(Animal):
    def __init__(self, world):
        super(Elephant,self).__init__(world, Diet.herbivore)
        self.health = 10
        self.speed = 15
        #self.precepts =

    def utility(self):
        pass

class Tiger(Animal):
    def __init__(self, world):
        super(Tiger,self).__init__(world, Diet.carnivore)
        self.health = 10
        self.speed = 36
        self.food = ['Elephant', 'Giraffe']
        #self.precepts =

class Giraffe(Animal):
    def __init__(self, world):
        super(Giraffe,self).__init__(world, Diet.herbivore)
        self.health = 10
        self.speed = 31
        self.food = ['Elephant', 'Giraffe']
        #self.precepts =
