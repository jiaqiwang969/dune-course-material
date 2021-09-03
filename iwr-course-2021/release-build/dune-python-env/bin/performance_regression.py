#!/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-python-env/bin/python

import pandas
import subprocess
import sys

class color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def parse_data():
    frame = pandas.read_csv('timings.csv', header=None, names=('exec', 'kernel', 'time'), delimiter=' ')
    data = frame.groupby(('exec', 'kernel'))['time'].min()

    return data


def run():
    subprocess.call("make -j2 build_tests".split())
    subprocess.call("rm timings.csv".split())
    for i in range(10):
        subprocess.call("ctest".split())


def regression_summary():
    # Get timings
    run()
    data1 = parse_data()

    # Switch to reference data
    subprocess.call(sys.argv[1:], shell=True)

    # Get reference timings
    run()
    data2 = parse_data()

    for key in data1.keys():
        exe, kernel = key
        diff = data1[exe][kernel] - data2[exe][kernel]
        rel = abs(diff / data2[exe][kernel])
        s = exe + '/' + kernel + ': ' + str(rel)
        c = ''
        if rel > 0.02:
            if diff > 0.:
                c = color.RED
            else:
                c = color.GREEN

        print(c + s + color.ENDC)


if __name__ == '__main__':
    regression_summary()
