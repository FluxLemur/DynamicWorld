import random
import sys
from terrain import *

# sys.argv[1] = height
# sys.argv[2] = height
CONFIG_PATH = './world_config/'

# TODO: generate biomes?
def generate_world(height, width):
    f1 = open(CONFIG_PATH + 'world.txt', 'w')
    #f2 = open(CONFIG_PATH + 'resources.txt', 'w')
    f3 = open(CONFIG_PATH + 'animals.txt', 'w')
    for x in range(width):
        for y in range(height):
            r = random.randint(0,3)         # index into terrain
            terrain = Terrains.terrains[r]()
            terrain.randomly_populate_resources()

            f1.write(str(r) + ' ')
            #resources = []
            #for r_str,resource in terrain.resources.iteritems():
            #    resources.append(str(random.randint(1, terrain.max_resources[r_str])))
            #f2.write(' '.join(resources) + '\n')
            if random.random() < 0.05:
                anim = random.randint(1,3)
            else:
                anim = 0
            f3.write(str(anim) + '\n')

        f1.write('\n')
    f1.close()
    #f2.close()
    f3.close()

generate_world(int(sys.argv[1]), int(sys.argv[2]))
