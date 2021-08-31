import itertools
import pandas
import matplotlib
import sys

matplotlib.use("PDF")

import matplotlib.pyplot as plt

filename = sys.argv[1]
fig, ax = plt.subplots()
width = 0.5

opframe = pandas.read_csv("./operations.csv",
                          header=None,
                          delimiter=" ",
                          names=("exec", "degree", "what", "ops"),
                          )

av = opframe[opframe.what == "alpha_volume_kernel"]
ask = opframe[opframe.what == "alpha_skeleton_kernel"]
deg = [i - 0.3 for i in sorted(av['degree'])]

_, y1 = list(itertools.izip(*sorted(itertools.izip(av['degree'], av['ops']))))
_, y2 = list(itertools.izip(*sorted(itertools.izip(ask['degree'], ask['ops']))))
y2 = [a+b for a, b in zip(y1, y2)]
y3 = [1.0] * len(deg)

r3 = ax.bar(deg, y3, width, color="grey")
r2 = ax.bar(deg, y2, width, color="blue")
r1 = ax.bar(deg, y1, width, color="red")

ax.set_ylabel("Percentage")
ax.set_xticks(sorted(av['degree']))
ax.set_xticklabels(["Q{}".format(k) for k in sorted(av['degree'])])

timeframe = pandas.read_csv("./timeratios.csv",
                            header=None,
                            delimiter=" ",
                            names=("exec", "degree", "what", "ops"),
                            )

av = timeframe[timeframe.what == "alpha_volume_kernel"]
ask = timeframe[timeframe.what == "alpha_skeleton_kernel"]
deg = [i + 0.3 for i in sorted(av['degree'])]

_, y1 = list(itertools.izip(*sorted(itertools.izip(av['degree'], av['ops']))))
_, y2 = list(itertools.izip(*sorted(itertools.izip(ask['degree'], ask['ops']))))
y2 = [a+b for a, b in zip(y1, y2)]
y3 = [1.0] * len(deg)

r3 = ax.bar(deg, y3, width, color="grey", label="PDELab overhead")
r2 = ax.bar(deg, y2, width, color="blue", label="Skeleton integrals")
r1 = ax.bar(deg, y1, width, color="red", label="Volume integrals")

ax.legend(loc=3,
          ncol=2,
          bbox_to_anchor=(0.1, 1., 1., .1),
          )

for x in av['degree']:
    ax.text(x, -0.09, "Flops", rotation=45, horizontalalignment="right")
    ax.text(x + 0.6, -0.09, "Time", rotation=45, horizontalalignment="right")

plt.savefig(filename)
