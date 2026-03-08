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
    options = opts.get("options", {})
    a = int(options['a'])
    b = int(options['b'])
    c = int(options['c'])
    metal = options['metal']
    anion = options['s']
    formula = f"{metal}{anion}2"

    atoms = ase_mx2(formula, options['kind'], size=(a, b, c))

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
