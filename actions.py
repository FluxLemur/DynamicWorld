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

class Direction:
    north = 0
    east  = 1
    south = 2
    west  = 3
    directions = [north, east, south, west]

    @staticmethod
    def random_direction():
        return random.choice(Direction.directions)

    @staticmethod
    def get_tuple(direction):
        ''' Returns the direction tuple in a grid with (0,0) at the top left,
            (horizontal, vertical) orientation '''
        if direction == Direction.north:
            return (-1,0)
        elif direction == Direction.south:
            return (1,0)
        elif direction == Direction.east:
            return (0,1)
        elif direction == Direction.west:
            return (0,-1)

class Move(Action):
    def __init__(self, direction=None):
        self.direction = direction

class Actions:
    actions = [Sleep, Drink, Eat, Move]

    @staticmethod
    def random_action():
        A = random.choice(Actions.actions)
        if A == Move:
            return Move(random.choice(Direction.directions))
        else:
            return A()
