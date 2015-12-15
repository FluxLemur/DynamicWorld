import matplotlib.pyplot as plt
import numpy as np

anim_steps = {'Tiger':[], 'Giraffe':[], 'Elephant':[]}
with open('data/superior_elephant.txt') as f:
    for line in f:
        split_line = line.strip().split()
        anim_steps[split_line[0]].append(int(split_line[1]))

N = len(anim_steps['Tiger'])
width = 0.5

fig, ax = plt.subplots()
t_bar = ax.bar(0, np.mean(anim_steps['Tiger']), width,
        yerr=np.std(anim_steps['Tiger']), color='orange')
g_bar = ax.bar(1, np.mean(anim_steps['Giraffe']), width,
        yerr=np.std(anim_steps['Giraffe']), color='yellow')
e_bar = ax.bar(2, np.mean(anim_steps['Elephant']), width,
        yerr=np.std(anim_steps['Elephant']), color='purple')

ax.legend((t_bar, g_bar, e_bar), ('Tiger', 'Giraffe', 'Elephant'), loc=2)
plt.title('Average number of steps survived by species')
plt.ylabel('Avg. steps alive (with std dev)')
plt.xlabel('Species')
plt.tick_params(labelbottom='off')
plt.show()
