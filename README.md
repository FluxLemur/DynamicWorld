# Dynamic Animal World

## Description
We propose to simulate a world in which animals interact with each other and the available resources. The world is represented as a grid of cells, each defined by terrain (desert, plain, forest, mountain) and resources. Animals roam the world, eating, resting, and interacting amongst each other. Resources such as food and water will be contested by competing animals, and increase/decrease dynamically over time. We model the animals as rational agents, such that we can effectively program their behaviors and draw parallels to areas in Artificial Intelligence.

In our initial implementation, animals will all be random instances of different species, each with various parameters such as health, hunger, and speed. Species will be parameterized by dietary restrictions (carnivore, omnivore, and herbivore) and by differences in their utility functions.

The end goal is a complex and fast-changing virtual world from which we can draw intuitive observations that reflect phenomena in the real animal planet.

## Approach
We will implement our project in Python. We will use a 2D graphics library to create a simple visualization of our world. The user interface will involve clicking on a cell to get information about it (such as the terrain, resources, and animals it contains), and further clicking on animal icons to get obtain more details about their status and parameters.

The environment is:
- Static
  - The state of the world does not change within a single time step.
- Partially observable
  - The agent knows everything about the terrain and resources of the cell it is currently in.
  - At the start of the simulation, the agent does not have any knowledge of the world.
  - The agent knows what other agents are present in its cell but does not have access to those animals’ parameters - such as energy and hunger.
- Stochastic
  - Resources in the world regenerate randomly.
- Discrete
  - There are a finite number of precepts and actions (directions to move, whether to eat, sleep, etc.).
- Multi-agent

An animal is a rational agent in that it has:
- Percepts
  - An animal will be able to observe the animals in its present cell, the resources in its cell, and the terrain it is in.
  - Precepts will vary from animal to animal, as some may be able to see more neighboring animals/resources, etc.
  - The agent stores an internal representation of the world, based on such previous percepts.
- Actions
  - Move, eat, rest.
  - The animal determines which action to perform by attempting to maximize its utility function while maintaining a valid state (some animals cannot travel into mountains, deserts, etc.).
- Goals
  - Maximizing utility (staying alive, low hunger, exploring the world).
  - Each component of the utility function will have a weight, which can vary between animal species (tiger values finding prey, and the gazelle avoids predators).
- Environment
  - As specified in the description section.

## Onwards
There are many possible additions to the project to make it more realistic and complex. One example, time permitting, is to implement the reproductive cycle, a prime opportunity for genetic algorithms!
