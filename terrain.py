import random

class Terrain:
    def __init__(self):
      # for colors, see http://wiki.tcl.tk/37701
      self.terrain_colors = {'Plains':'spring green', 'Forest':'forest green', \
      'Desert':'gold', 'River':'light sky blue'}
      self.terrain_resources = {'Plains': ['Water', 'Grass'], 'Desert':[], \
      'Forest':['Trees', 'Leaves', 'Bugs'], 'River': ['Water', 'Fish']}

    def random_terrain(self):
      t = random.sample(self.terrain_colors, 1)[0]
      if self.terrain_resources[t] == []:
        return(t, 'None')
      else:
        s = ''
        for resource in self.terrain_resources[t]:
          r = random.randint(3,10)
          s += resource + ': ' + str(r) + '\n'
        return [t,s]

    def get_color(self, terrain):
      return self.terrain_colors[terrain]