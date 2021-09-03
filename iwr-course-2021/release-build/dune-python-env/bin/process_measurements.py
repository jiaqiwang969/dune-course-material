#!/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-python-env/bin/python

import os
import pandas
import re


def join_csv_files():
    with open('timings.csv', 'w') as out:
        for f in os.listdir(os.getcwd()):
            match = re.match(".*rank-([0-9]*).*", f)
            if match:
                for line in open(f, 'r'):
                    out.write("{} {}".format(match.group(1), line))


def get_reference_kernel(kernel):
    if kernel.startswith("alpha"):
        return "residual_evaluation"
    if kernel.startswith("jacobian_apply"):
        return "apply_jacobian"
    return kernel


def get_reference_integral_kernel(kernel):
    if kernel.startswith("alpha") and len(kernel.split("_")) == 4:
        return "_".join(kernel.split("_")[:-1])
    if kernel.startswith("jacobian_apply") and len(kernel.split("_")) == 5:
        return "_".join(kernel.split("_")[:-1])
    return kernel


def get_siblings_kernel(kernel):
    s = kernel.split("_")
    if (kernel.startswith("alpha") and len(s) == 4) or (kernel.startswith("jacobian_apply") and len(s) == 5):
        for suffix in ["setup", "stage1", "quadratureloop", "stage3"]:
            yield "_".join(s[:-1] + [suffix])
    else:
        yield kernel

def calculate_operations_percentage():
    frame = pandas.read_csv('timings.csv', header=None, names=('rank', 'level', 'ident', 'kernel', 'what', 'value'), delimiter=' ')
    ops = frame[frame.what != "time"]
    ops = ops.groupby(('rank', 'ident', 'kernel'))['value'].max().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()

    with open('operations.csv', 'w') as out:
        for key in ops.keys():
            ident, kernel = key
            degree = re.match(".*deg([0-9]*).*", ident).group(1)
            out.write(" ".join([ident, degree, kernel, str(ops[ident][kernel] / ops[ident][get_reference_kernel(kernel)]) + "\n"]))


def calculate_times_percentage():
    frame = pandas.read_csv('timings.csv', header=None, names=('rank', 'level', 'ident', 'kernel', 'what', 'value'), delimiter=' ')

    time4 = frame[(frame.what == "time") & (frame.level == 4)]
    time4 = time4.groupby(('rank', 'ident', 'kernel'))['value'].min().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()
    time3 = frame[(frame.what == "time") & (frame.level == 3)]
    time3 = time3.groupby(('rank', 'ident', 'kernel'))['value'].min().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()

    with open('timeratios.csv', 'w') as out:
        for key in time4.keys():
            ident, kernel = key
            degree = re.match(".*deg([0-9]*).*", ident).group(1)
            stage = time4[ident][kernel]
            sum4 = sum(time4[ident][k] for k in get_siblings_kernel(kernel))
            int3 = time3[ident][get_reference_integral_kernel(kernel)]
            ref =  time3[ident][get_reference_kernel(kernel)]
            out.write(" ".join([ident, degree, kernel, str(float(stage*int3) / float(sum4*ref)) + "\n"]))


def calculate_floprate():
    frame = pandas.read_csv('timings.csv', header=None, names=('rank', 'level', 'ident', 'kernel', 'what', 'value'), delimiter=' ')
    time = frame[frame.what == "time"]
    ops = frame[frame.what != "time"]

    time = time.groupby(('rank', 'ident', 'kernel'))['value'].min().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()
    ops = ops.groupby(('rank', 'ident', 'kernel'))['value'].max().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()

    with open('floprates.csv', 'w') as out:
        for key in time.keys():
            ident, kernel = key
            degree = re.match(".*deg([0-9]*).*", ident).group(1)
            operations = ops[ident][kernel]
            out.write(" ".join([ident, degree, kernel, str((operations / time[ident][kernel]) / 1e9)]) + "\n")


def calculate_doftimes():
    frame = pandas.read_csv('timings.csv', header=None, names=('rank', 'level', 'ident', 'kernel', 'what', 'value'), delimiter=' ')
    dofs = frame[frame.what == "dofs"]
    time = frame[frame.what == "time"]

    dofs = dofs.groupby(('rank', 'ident', 'kernel'))['value'].max().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()
    time = time.groupby(('rank', 'ident', 'kernel'))['value'].min().to_frame().reset_index().groupby(('ident', 'kernel'))['value'].max()

    with open('doftimes.csv', 'w') as out:
        for key in time.keys():
            ident, kernel = key
            degree = re.match(".*deg([0-9]*).*", ident).group(1)
            out.write(" ".join([ident, degree, kernel, str(dofs[ident]["dofs"] / time[ident][kernel] / 1e6)]) + "\n")


if __name__ == '__main__':
    join_csv_files()
    calculate_floprate()
    calculate_doftimes()
    calculate_operations_percentage()
    calculate_times_percentage()
