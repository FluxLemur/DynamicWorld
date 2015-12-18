import random

class Action(object):
    pass

class Eat(Action):
    def __init__(self, food=None, is_animal=False):
        self.food = food
        self.is_animal = is_animal

class Sleep(Action):
    pass

class Drink(Action):
    pass

class Mate(Action):
    def __init__(self, partner):
        self.partner = partner

class Direction:
    north = (-1,0)
    east  = (0,1)
    south = (1,0)
    west  = (0,-1)
    directions = [north, east, south, west]

    @staticmethod
    def random_direction():
        return random.choice(Direction.directions)

class Move(Action):
    def __init__(self, direction=None):
        self.direction = direction

class Actions:
    actions = [Sleep, Drink, Eat, Move] # TODO: add Mate

    @staticmethod
    def random_action():
        A = random.choice(Actions.actions)
        if A == Move:
            return Move(random.choice(Direction.directions))
        else:
            return A()
