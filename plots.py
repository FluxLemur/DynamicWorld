import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator
import numpy as np
from scipy.stats import sem
from animal import DeathCause as DC
import sys

data_file = sys.argv[1] if len(sys.argv) > 1 else 'data/temp.txt'
time_file = sys.argv[2] if len(sys.argv) > 2 else 'data/temp_timeseries.txt'

survivals = {'Tiger':[], 'Giraffe':[], 'Elephant':[]}

causes = {DC.hunger: 0, DC.eaten: 0, DC.thirst:0}
death_causes = {'Tiger':causes.copy(), 'Giraffe':causes.copy(), 'Elephant':causes.copy()}
timeseries = {'Tiger':[], 'Giraffe':[], 'Elephant':[]}

with open(data_file) as f:
    f.readline()  # the first line should contain a comment
    for line in f:
        split_line = line.strip().split()
        species, steps, cause = split_line
        survivals[species].append(int(steps))
        death_causes[species][cause] += 1

with open(time_file) as f:
    f.readline()
    for line in f:
        split_line = line.strip().split()
        g, e, t = split_line
        timeseries['Giraffe'].append(int(g))
        timeseries['Elephant'].append(int(e))
        timeseries['Tiger'].append(int(t))

N = len(survivals['Tiger'])

def plot_survival():
    width = 0.5
    fig, ax = plt.subplots()
    t_bar = ax.bar(0, np.mean(survivals['Tiger']), width,
            yerr=sem(survivals['Tiger']), color='orange')
    g_bar = ax.bar(1, np.mean(survivals['Giraffe']), width,
            yerr=sem(survivals['Giraffe']), color='yellow')
    e_bar = ax.bar(2, np.mean(survivals['Elephant']), width,
            yerr=sem(survivals['Elephant']), color='purple')

    #ax.legend((t_bar, g_bar, e_bar), ('Tiger', 'Giraffe', 'Elephant'), loc=2)

    ax.set_xticklabels(['Tiger', 'Giraffe', 'Elephant'])

    tick_locator = IndexLocator(1, 0.25)
    ax.xaxis.set_major_locator(tick_locator)

    plt.title('Average number of steps survived by species (N=%d)' % (N*3))
    plt.ylabel('Avg. steps alive (with standard error)')
    plt.show()

def plot_death_causes():
    for species,causes in death_causes.iteritems():
        labels = DC.hunger, DC.eaten, DC.thirst
        sizes = [causes[DC.hunger], causes[DC.eaten], causes[DC.thirst]]
        colors = ['orange', 'red', 'blue']

        plt.pie(sizes, labels=labels, colors=colors,
                        autopct='%1.1f%%', startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        #plt.axis('equal')
        plt.title('Death causes for %ss' % species)
        plt.show()

def plot_timeseries():
    plt.plot(timeseries['Giraffe'], linewidth=4, color='yellow', label='Giraffe')
    plt.plot(timeseries['Elephant'], linewidth=4, color='purple', label='Elephant')
    plt.plot(timeseries['Tiger'], linewidth=4, color='orange', label='Tiger')
    plt.legend(loc=1)

    plt.title('Number of Animals over time')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Animals Alive')
    plt.show()

plot_timeseries()
plot_survival()
plot_death_causes()
