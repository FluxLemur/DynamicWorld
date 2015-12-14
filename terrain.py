import random
from collections import Counter
from resources import Resources

# Note: for colors, see http://wiki.tcl.tk/37701

R = Resources

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

class Plains(Terrain):
    def __init__(self):
        super(Plains,self).__init__('spring green')
        self.resources = {R.grass: 0}
        self.max_resources = {R.grass: 10}

class Desert(Terrain):
    def __init__(self):
        super(Desert,self).__init__('gold')
        self.resources = {}
        self.max_resources = {}

class Forest(Terrain):
    def __init__(self):
        super(Forest,self).__init__('forest green')
        self.resources = {R.fruit: 0, R.leaves: 0}
        self.resources = {R.fruit: 5, R.leaves: 5}

class River(Terrain):
    def __init__(self):
        super(River,self).__init__('light sky blue')
        self.resources = {R.water: 10, R.fish: 5}

class Terrains:
    terrains = [Plains, Desert, Forest, River]

    @staticmethod
    def random_terrain():
        terrain = random.choice(Terrains.terrains)()
        terrain.randomly_populate_resources()
        return terrain
