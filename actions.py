import random

class Action:
    pass

class Eat(Action):
    def __init__(self, food):
        self.food = food

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
    def get_tuple(direction):
        ''' Returns the direction tuple in a grid with (0,0) at the top left,
            (horizontal, vertical) orientation '''
        if direction == north:
            return (-1,0)
        elif direction == south:
            return (1,0)
        elif direction == east:
            return (0,1)
        elif direction == west:
            return (0,-1)

class Move(Action):
    def __init__(self, direction):
        self.direction = direction

class RandomMove(Move):
    def __init__(self):
        super(RandomMove,self).__init__(self, random.choice(Directions.directions))

class Actions:
    actions    = [Sleep, Drink, Eat, RandomMove]

    @staticmethod
    def random_action_cons():
        a = random.choice(actions)
        if type(a) == list:
            return random.choice(a)
        else:
            return a
