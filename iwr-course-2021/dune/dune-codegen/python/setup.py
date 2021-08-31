#!/usr/bin/env python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='dune.codegen',
      version='0.1',
      namespace_packages=['dune'],
      description='Performance optimizing form compiler for the Dune project',
      author='Dominic Kempf <dominic.kempf@iwr.uni-heidelberg.de>',
      url='https://gitlab.dune-project.org/dominic/dune-codegen.git',
      python_requires='>=3',
      packages=['dune.codegen',
                'dune.codegen.blockstructured',
                'dune.codegen.cgen',
                'dune.codegen.generation',
                'dune.codegen.loopy',
                'dune.codegen.loopy.transformations',
                'dune.codegen.pdelab',
                'dune.codegen.pdelab.driver',
                'dune.codegen.sumfact',
                'dune.codegen.ufl',
                'dune.codegen.ufl.transformations',
                ],
      install_requires=['sympy', 'frozendict', 'pytest', 'pytest-pep8', 'filelock', 'cerberus', 'pyaml'],
      cmdclass={'test': PyTest},
      entry_points = {
        "console_scripts": [
            "generate_operators = dune.codegen.compile:entry_generate_operators",
            "generate_driver = dune.codegen.compile:entry_generate_driver",
            "generate_driver_block = dune.codegen.compile:entry_generate_driver_block",
            "show_options = dune.codegen.options:show_options",
        ],
      },
      include_package_data=True,
)
