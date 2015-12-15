import random
from collections import Counter
from resources import Resources as R

GENERATE_RESOURCE = 0.9999

# Note: for colors, see http://wiki.tcl.tk/37701
class Terrain(object):
    def __init__(self, color):
        self.color = color
        self.resources = {}
        self.max_resources = {}

    def get_color(self):
        return self.color

    def randomly_populate_resources(self):
        for resource in self.resources.iterkeys():
            self.resources[resource] = random.randint(3,10)

    def resource_string(self):
        res = ''
        for resource,count in self.resources.iteritems():
            res += '{}: {}\n'.format(resource, count)
        return res

    def __str__(self):
        return type(self).__name__

    def add_resource(self, r):
        assert r in self.resources
        self.resources[r] += 1

    def step_resources(self):
        for r,curr_r in self.resources.iteritems():
            if curr_r < self.max_resources[r]:
                if random.random() > GENERATE_RESOURCE:
                    self.resources[r] += 1

    def contains(self, r):
        # returns whether this terrain contains the resource [r]
        return r in self.resources and self.resources[r] > 0

    def consume_resource(self, r):
        assert self.contains(r)
        self.resources[r] -= 1

    def no_resources(self):
        for count in self.resources.itervalues():
            if count > 0:
                return False
        return True

class Plains(Terrain):
    def __init__(self):
        super(Plains,self).__init__('spring green')
        self.resources = {R.grass: 5}
        self.max_resources = {R.grass: 10}

class Desert(Terrain):
    def __init__(self):
        super(Desert,self).__init__('gold')
        self.resources = {}
        self.max_resources = {}

class Forest(Terrain):
    def __init__(self):
        super(Forest,self).__init__('forest green')
        self.resources = {R.fruit: 2, R.leaves: 2}
        self.max_resources = {R.fruit: 5, R.leaves: 5}

class River(Terrain):
    def __init__(self):
        super(River,self).__init__('light sky blue')
        self.resources = {R.water: 10, R.fish: 5}
        self.max_resources = {R.water: 20, R.fish: 5}

class Terrains:
    terrains = [Desert, Plains, Forest, River]

    @staticmethod
    def random_terrain():
        terrain = random.choice(Terrains.terrains)()
        terrain.randomly_populate_resources()
        return terrain
