# -*- coding: utf-8 -*-
"""
Created on 2019/11/20 15:24:39

@author: Mon
"""

from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("ctools/ccctest.pyx"))