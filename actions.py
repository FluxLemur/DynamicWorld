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

class Move(Action):
    def __init__(self, direction):
        self.direction = direction

class RandomMove(Move):
    def __init__(self):
        super(RandomMove,self).__init__(self, random.choice(Directions.directions))

class Actions:
    move_north = Move(Direction.north)
    move_east  = Move(Direction.east)
    move_south = Move(Direction.south)
    move_west  = Move(Direction.west)
    sleep      = Sleep()
    actions = [Sleep, Drink, Eat, RandomMove]

    @staticmethod
    def random_action_cons():
        a = random.choice(actions)
        if type(a) == list:
            return random.choice(a)
        else:
            return a
