"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import os
import tempfile

import ase.io
from ase.build import mx2 as ase_mx2


def generate(opts):
    a = int(opts['a'])
    b = int(opts['b'])
    c = int(opts['c'])
    metal = opts['metal']
    s = opts['s']
    formula = f"{metal}{s}2"

    atoms = ase_mx2(formula, opts['kind'], size=(a, b, c))

    fd, name = tempfile.mkstemp(".xyz")
    os.close(fd)

    ase.io.write(name, atoms, format="extxyz")

    with open(name) as f:
        xyz_data = f.read()
    os.remove(name)

    return xyz_data


def run(avo_input):
    return {
        'append': True,
        'moleculeFormat': 'xyz',
        'xyz': generate(avo_input),
    }
