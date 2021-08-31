#!/usr/bin/env python

import itertools
import pandas
import matplotlib
import sys

matplotlib.use("PDF")

from matplotlib import pyplot as plt

what = sys.argv[1]
title = sys.argv[2]
filename = title.lower().replace(" ", "_") + ".pdf"

flopframe = pandas.read_csv("./floprates.csv", header=None, delimiter=" ", names=("exec", "degree", "what", "GFlops"))
flopframe = flopframe[flopframe.what == what]

timeframe = pandas.read_csv("./doftimes.csv", header=None, delimiter=" ", names=("exec", "degree", "what", "DOFs"))
timeframe = timeframe[timeframe.what == what]

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
x, y = list(itertools.izip(*sorted(itertools.izip(flopframe['degree'], flopframe['GFlops']))))
ax1.plot(x, y, "b-", x, y, "bo")
x, y = list(itertools.izip(*sorted(itertools.izip(timeframe['degree'], timeframe['DOFs']))))
ax2.plot(x, y, "r-", x, y, "ro")

ax1.set_xlabel("Polynomial degree")
ax1.set_ylabel("GFlops /s", color="b")
ax2.set_ylabel("MDOFs / s", color="r")
plt.title(title)

plt.savefig(filename)
