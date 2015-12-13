import random
import sys

# sys.argv[1] = height
# sys.argv[2] = height

def generate_world(height, width):
  f = open('world.txt', 'w')
  for x in range(width):
    for y in range(height):
      r = random.randint(0,3)     # index into terrain
      f.write(str(r) + ' ')
    f.write('\n')
  f.close()

#generate_world(int(sys.argv[1]), int(sys.argv[2]))