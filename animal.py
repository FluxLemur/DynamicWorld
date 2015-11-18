class Elephant:
  def __init__(self, size):
    self.health = 10
    self.hunger = 5
    self.speed = 15
    self.dietary = 'Herbivore'
    #self.precepts =

  def act(self):
    r = random.randint(0,3)
    if r == 0:
        #sleep
    if r == 1:
        #eat
    if r == 2:
        #no-op
    else:
        direction = random.randint(0,3)
        if direction == 0:
            #move north
        if direction == 1:
            #move east
        if direction == 2:
            #move south
        else:
            #move west

  #the animal's utility function
  def utility(self):
    return

class Tiger:
    self.health = 10
    self.hunger = 5
    self.speed = 36
    self.dietary = 'Carnivore'
    self.food = ['Elephant', 'Giraffe']
    #self.precepts =

class Giraffe:
    self.health = 10
    self.hunger = 5
    self.speed = 31
    self.dietary = 'Herbivore'
    #self.precepts =

class Animal:
  def __init__(self, world):
    #either Giraffe, Elephant or Tiger
    self.world = world
    self.type =
    #the cell the animal is currently in
    self.cell =
    #eating, moving, resting ...
    self.state =

    #animal has some internal rep. of the world
