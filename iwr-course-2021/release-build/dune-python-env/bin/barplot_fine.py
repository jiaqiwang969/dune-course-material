import itertools
import pandas
import matplotlib
import sys

matplotlib.use("PDF")

import matplotlib.pyplot as plt

filename = sys.argv[1]
fig, ax = plt.subplots()
if len(sys.argv) > 2:
    # Use 0.35 - 0.4 for a 1-10 plot
    width = float(sys.argv[2])
else:
    width = 0.5

opframe = pandas.read_csv("./operations.csv",
                          header=None,
                          delimiter=" ",
                          names=("exec", "degree", "what", "ops"),
                          )


av1 = opframe[opframe.what == "alpha_volume_kernel_stage1"]
av2 = opframe[opframe.what == "alpha_volume_kernel_quadratureloop"]
av3 = opframe[opframe.what == "alpha_volume_kernel_stage3"]
ask1 = opframe[opframe.what == "alpha_skeleton_kernel_stage1"]
ask2 = opframe[opframe.what == "alpha_skeleton_kernel_quadratureloop"]
ask3 = opframe[opframe.what == "alpha_skeleton_kernel_stage3"]
setup1 = opframe[opframe.what == "alpha_volume_kernel_setup"]
setup2 = opframe[opframe.what == "alpha_skeleton_kernel_setup"]
deg = [i - width/1.8 for i in sorted(av1['degree'])]


def update(frame, result=None):
    _, y = list(itertools.izip(*sorted(itertools.izip(frame['degree'], frame['ops']))))
    if result is None:
        return y
    else:
        return [a+b for a, b in zip(y, result)]


y1 = update(av1)
y2 = update(av2, y1)
y3 = update(av3, y2)
y4 = update(setup1, y3)
y5 = update(ask1, y4)
y6 = update(ask2, y5)
y7 = update(ask3, y6)
y8 = update(setup2, y7)
y9 = [1.0] * len(deg)

r9 = ax.bar(deg, y9, width, color="grey")
r8 = ax.bar(deg, y8, width, color="xkcd:light green")
r7 = ax.bar(deg, y7, width, color="xkcd:light blue")
r6 = ax.bar(deg, y6, width, color="xkcd:blue")
r5 = ax.bar(deg, y5, width, color="xkcd:dark blue")
r4 = ax.bar(deg, y4, width, color="green")
r3 = ax.bar(deg, y3, width, color="yellow")
r2 = ax.bar(deg, y2, width, color="orange")
r1 = ax.bar(deg, y1, width, color="red")

ax.set_ylabel("Percentage")
ax.set_xticks(sorted(av1['degree']))
ax.set_xticklabels(["Q{}".format(k) for k in sorted(av1['degree'])])

timeframe = pandas.read_csv("./timeratios.csv",
                            header=None,
                            delimiter=" ",
                            names=("exec", "degree", "what", "ops"),
                            )

av1 = timeframe[timeframe.what == "alpha_volume_kernel_stage1"]
av2 = timeframe[timeframe.what == "alpha_volume_kernel_quadratureloop"]
av3 = timeframe[timeframe.what == "alpha_volume_kernel_stage3"]
ask1 = timeframe[timeframe.what == "alpha_skeleton_kernel_stage1"]
ask2 = timeframe[timeframe.what == "alpha_skeleton_kernel_quadratureloop"]
ask3 = timeframe[timeframe.what == "alpha_skeleton_kernel_stage3"]
setup1 = timeframe[timeframe.what == "alpha_volume_kernel_setup"]
setup2 = timeframe[timeframe.what == "alpha_skeleton_kernel_setup"]
deg = [i + width/1.8 for i in sorted(av1['degree'])]

y1 = update(av1)
y2 = update(av2, y1)
y3 = update(av3, y2)
y4 = update(setup1, y3)
y5 = update(ask1, y4)
y6 = update(ask2, y5)
y7 = update(ask3, y6)
y8 = update(setup2, y7)
y9 = [1.0] * len(deg)

r9 = ax.bar(deg, y9, width, label="PDELab overhead", color="grey")
r8 = ax.bar(deg, y8, width, label="Geometry evaluations Skeleton", color="xkcd:light green")
r7 = ax.bar(deg, y7, width, label="Skeleton, backward SF", color="xkcd:light blue")
r6 = ax.bar(deg, y6, width, label="Skeleton, Quadrature", color="xkcd:blue")
r5 = ax.bar(deg, y5, width, label="Skeleton, forward SF", color="xkcd:dark blue")
r4 = ax.bar(deg, y4, width, label="Geometry evaluations Volume", color="green")
r3 = ax.bar(deg, y3, width, label="Volume, backward SF", color="yellow")
r2 = ax.bar(deg, y2, width, label="Volume, Quadrature", color="orange")
r1 = ax.bar(deg, y1, width, label="Volume, forward SF", color="red")

lgd = ax.legend(loc=3,
                ncol=2,
                bbox_to_anchor=(0.05, 1., 1., .1),
                )

texts = []
for x in av1['degree']:
    texts.append(ax.text(x, -0.09, "Flops", rotation=45, horizontalalignment="right"))
    texts.append(ax.text(x + width, -0.09, "Time", rotation=45, horizontalalignment="right"))

plt.savefig(filename,
            bbox_extra_artists=tuple(texts) + (lgd,),
            bbox_inches='tight')
