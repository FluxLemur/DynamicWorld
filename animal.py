import random
from actions import *

class Diet:
    herbivore = [grass, fruit, leaves]
    carnivore = []
    omnivore  = [fish, grass, fruit, leaves]

class Animal:
    def __init__(self, world, diet):
        self.world = world
        self.diet = diet
        self.color = 'Black'
        self.hunger = 0             # hunger level (0 - 10 scale)
        self.energy = 10            # energy level (0 - 10 scale)
        self.thirst = 0             # thirst leve (0 - 10 scale)
        self.attacks = 0            # number of attacks the animal has been subject to

        self.cell = None            # the cell the animal is currently in

        # animal has some internal rep. of the world

    def update_hunger(self):
        if self.hunger < 2:
            self.hunger = 0
        else:
            self.hunger -= 2

    def update_thirst(self):
        if self.thirst < 2:
            self.thirst = 0
        else:
            self.thirst -= 2

    def update_energy(self):
        if self.energy > 8:
            self.energy = 10
        else:
            self.energy += 2

    # choose an action
    def act(self):
        # randomly select an action
        action_cons = Actions.random_action_cons()

        if action_cons == Eat:
            for food in self.diet:
                if self.cell.contains_resource(food):
                    self.update_hunger()
                    return Eat(food)

            # no food to eat - sleep instead
            self.update_energy()
            return Sleep()

        elif action_cons == Drink:
            if self.cell.contains_resource(water):
                self.update_thirst()
                return Drink()
            else:      # no water to drink - sleep instead
                self.update_energy()
                return Sleep()

        elif action_cons == Sleep:
            self.update_energy()
            return Sleep()

class Elephant(Animal):
    def __init__(self, world):
        super(Elephant,self).__init__(world, Diet.herbivore)
        self.prey = []
        self.color = 'Purple'
        #self.precepts =

class Tiger(Animal):
    def __init__(self, world):
        super(Tiger,self).__init__(world, Diet.carnivore)
        self.prey = ['Elephant', 'Giraffe']
        self.color = 'Orange'
        #self.precepts =

class Giraffe(Animal):
    def __init__(self, world):
        super(Giraffe,self).__init__(world, Diet.herbivore)
        self.prey = []
        self.color = 'Yellow'
        #self.precepts =
