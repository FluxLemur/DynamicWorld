import random
import sys
from terrain import *

# sys.argv[1] = height
# sys.argv[2] = height

def generate_world(height, width):
  f1 = open('world.txt', 'w')
  f2 = open('resources.txt', 'w')
  f3 = open('animals.txt', 'w')
  for x in range(width):
    for y in range(height):
      r = random.randint(0,3)     # index into terrain
      terrain = Terrains.terrains[r]()
      terrain.randomly_populate_resources()

      f1.write(str(r) + ' ')
      for resource in terrain.resources.iterkeys():
        f2.write(str(random.randint(3, 10)) + ' ')
      f2.write('\n')

    f1.write('\n')
  f1.close()
  f2.close()
  f3.close()

generate_world(int(sys.argv[1]), int(sys.argv[2]))
