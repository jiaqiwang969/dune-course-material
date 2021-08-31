#
# Call with result as the first argument and then argument tuples of data directory, core number and name, like:
# python socketcompare.py result.pdf ~/results/knl 68 "Knights Landing" ~/results/haswell 16 "Haswell"
#

import itertools
import pandas
import matplotlib
import os
import sys

matplotlib.use("PDF")

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()


def add_measurements(path=None, what="residual_evaluation", cores=1, label=None, **kwargs):
    assert path
    frame = pandas.read_csv(os.path.join(path, "floprates.csv"),
                            header=None,
                            delimiter=" ",
                            names=("exec", "degree", "what", "flops"),
                            )

    frame = frame[frame.what == what]

    x, y = list(itertools.izip(*sorted(itertools.izip(frame['degree'], frame['flops']))))
    y = [float(cores)*i for i in y]
    ax1.plot(x, y, "r-", label=label, **kwargs)
    ax1.plot(x, y, "ro", **kwargs)

    frame = pandas.read_csv(os.path.join(path, "doftimes.csv"),
                            header=None,
                            delimiter=" ",
                            names=("exec", "degree", "what", "time"),
                            )

    frame = frame[frame.what == what]

    x, y = list(itertools.izip(*sorted(itertools.izip(frame['degree'], frame['time']))))
    y = [float(cores)*i for i in y]
    ax2.plot(x, y, "b-", label=label, **kwargs)
    ax2.plot(x, y, "bo", **kwargs)

styles = ['solid', 'dashed', 'dotted']

i = 2
while i < len(sys.argv):
    add_measurements(path=sys.argv[i],
                     cores=sys.argv[i+1],
                     label=sys.argv[i+2],
                     linestyle=styles[(i-2) // 3])
    i = i + 3

ax1.set_xlabel("Polynomial degree", fontsize=20)
ax1.set_ylim(bottom=0)
ax2.set_ylim(bottom=0)
ax1.set_ylabel("GFlops /s", color="b", fontsize=20)
ax2.set_ylabel("MDOF / s", color="r", fontsize=20)

plt.legend(loc="upper left")

plt.savefig(sys.argv[1])