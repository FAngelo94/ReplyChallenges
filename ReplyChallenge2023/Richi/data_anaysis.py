import matplotlib.pyplot as plt
import numpy as np
from Richi.problem import Problem
import os
from matplotlib import colors


files = sorted(os.listdir("data"))
problems = [Problem.from_file(f"data/{file}") for file in files[1:]]


# plot scalar data of all the problem in a histogram
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
def plot_histogram(groups, bars):
    fig, ax = plt.subplots(layout='constrained')

    x = np.arange(len(groups))  # the label locations
    width = 1/(len(bars) + 1)  # the width of the bars
    multiplier = 0

    for attribute, measurement in bars.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Length (mm)')
    ax.set_title('Problems statistics')
    ax.set_xticks(x + width, groups, rotation=90)
    ax.legend(loc='best', ncols=1)
    # ax.set_ylim(0, 500000)

    plt.show()


## plot distribution of a group af attributes
def plot_single_distribution(problems_list, attribute_name):
    fig, axs = plt.subplots(len(problems_list), 1, tight_layout=True)

    for i, problem in enumerate(problems):
        problem_name = problem.name
        distribution = getattr(problem, attribute_name)
        axs[i].hist(distribution, bins=100)
        axs[i].set_title(f'{problem_name} {attribute_name}')

    plt.show()


def plot_two_distribution(problems_list, attribute_name1, atrribute_name2):
    fig, axs = plt.subplots(len(problems_list), 1, figsize=(5, 5*len(problems_list)), tight_layout=True)

    for i, problem in enumerate(problems):
        problem_name = problem.name
        dist1 = getattr(problem, attribute_name1)
        dist2 = getattr(problem, atrribute_name2)
        axs[i].hist2d(dist1, dist2, bins=40, norm=colors.LogNorm())
        axs[i].set_title(f'{problem_name} {attribute_name1} vs {atrribute_name2}')

    plt.show()


groups_a = ["Row", "Column", "n snakes"]
bar_a = {
   f"{p.name}": [p.R, p.C, p.S] for p in problems
}
groups_b = ["Avg Snake length", "Min Snake length", "Max Snake length"]
bar_b = {
   f"{p.name}": [np.median(p.Slen), np.min(p.Slen), np.max(p.Slen)] for p in problems
}
# groups_c = ["Desc1", "Desc2", "Desc3", "Desc4"]
# bar_c = {
#    f"{p.name}": [np.median(p.X), np.median(p.X), np.median(p.X), np.median(p.X)] for p in problems
# }

plot_histogram(groups_a, bar_a)
plot_histogram(groups_b, bar_b)
# plot_histogram(groups_c, bar_c)
#
plot_single_distribution(problems, "Slen")
# plot_single_distribution(problems, "attr")
# plot_single_distribution(problems, "attr")
# plot_single_distribution(problems, "attr")
#
# plot_two_distribution(problems, "attr1", "attr2")

for p in problems:
    g = p.grid
    g[g != 99999] = 0
    plt.matshow(g)
    plt.colorbar()
    plt.title(f"{p.name} grid")
    plt.show()

for p in problems:
    g = p.grid
    plt.matshow(p.grid)
    plt.colorbar()
    plt.show()