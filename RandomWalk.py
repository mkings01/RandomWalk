#  Random Walk
#
# To run this script you'll need the versions of packages listed in 
#  requirements.txt
#   eg 'pip install -r requirements.txt'
# The script was tested with Python 3.11.9

import random
# import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from tqdm import tqdm

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
CARDINAL_DIRECTIONS = [NORTH,EAST,SOUTH,WEST]

MOVE = 1
STAY = 2
MOVE_OPTIONS = [MOVE,STAY]

class CurrentWorldState:
    def __init__(self,max_x,max_y):
        self.max_x = max_x
        self.range_x = self.max_x * 2 + 1
        self.max_y = max_y
        self.range_y = self.max_y * 2 + 1
        self.walker_total = 0
        self.walker_counts = [[0 for x in range(self.range_x)] for y in range(self.range_y)]
    def add_walker(self,walker):
        adjusted_x = walker.x + max_x
        adjusted_y = walker.y + max_y
        self.walker_counts[adjusted_x][adjusted_y] +=1
        self.walker_total += 1
    def add_walkers(self,walkers):
        for walker in walkers:
            self.add_walker(walker)
    def plot(self):
        current_fig, current_plot_ax1 = plt.subplots()
        extent = [-self.max_x, self.max_x, -self.max_y, self.max_y]
        colormesh = current_plot_ax1.imshow(self.walker_counts,
                                            extent=extent)
        current_plot_ax1.set_title("Final random walker distribution, total count=" + str(self.walker_total))
        current_plot_ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        current_plot_ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        colorbar = plt.colorbar(mappable=colormesh, 
                                orientation='vertical', 
                                label='counts',
                                format=lambda x, 
                                        _: f'{x:.0f}')

class RandomWalker:
    def __init__(self):
        self.x = 0
        self.y = 0
    def walk_once(self, max_x, max_y):
        # pick a random direction
        move_option = random.choice(MOVE_OPTIONS)
        
        if move_option == STAY:
            pass
        elif move_option == MOVE:
            direction = random.choice(CARDINAL_DIRECTIONS)
            # move 1 space in that direction
            if direction==NORTH:
                self.y += 1
            elif direction==EAST:
                self.x += 1
            elif direction==SOUTH:
                self.y -= 1
            elif direction==WEST:
                self.x -= 1
            else:
                # This shouldn't happen
                raise("attempted to move in an illegal direction")
            # move walker back inside the limits if it left
            if(self.x > max_x):
                self.x = max_x
            elif(self.x < -max_x):
                self.x = -max_x
            elif(self.y > max_y):
                self.y = max_y
            elif(self.y < -max_y):
                self.y = -max_y
        else:
            # This shouldn't happen
            raise("attempted a third movement option")

class RandomWalkSimulation:
    def __init__(self, num_walkers, max_x, max_y):
        self.random_walkers = [RandomWalker() for i in range(num_walkers)]
        self.max_x = max_x
        self.max_y = max_y
        self.final_world_state = CurrentWorldState(max_x=self.max_x,max_y=self.max_y)
    def iterate_simulation(self):
        for random_walker in self.random_walkers:
            random_walker.walk_once(max_x=max_x, max_y=max_y)
    def run_simulation(self, steps):
        for i in range(steps):
            self.iterate_simulation()

if __name__ == "__main__":
    # TODO: add argument handling
    num_iterations = 200
    num_walkers_array = [10, 100, 1000, 10000, 100000]
    max_x = max_y = 100
    for num_walkers in tqdm(num_walkers_array,
                            '├Scenarios progress',
                            position=0):
        current_simulation = RandomWalkSimulation(num_walkers=num_walkers,
                                                  max_x=max_x,
                                                  max_y=max_y)
        current_simulation.run_simulation(num_iterations)
        current_simulation.final_world_state.add_walkers(current_simulation.random_walkers)
        current_simulation.final_world_state.plot()

        
    plt.show()