#!/usr/bin/env python

#
# This is a bogus package to install all the python scripts that we need
# in the bin folder into the Dune virtualenv.
#

from setuptools import setup


setup(name='dunecodegencoveniencescripts',
      version='0.1',
      description='Some convenience scripts',
      author='Dominic Kempf <dominic.kempf@iwr.uni-heidelberg.de>',
      install_requires=['pandas', 'matplotlib'],
      scripts=['performance_regression.py',
               'plot_measurements.py',
               'process_measurements.py',
               'barplot_coarse.py',
               'barplot_fine.py',
               'socketcompare.py',
               ])
