"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import os
import tempfile

import ase.io
from ase.build import nanotube as ase_nanotube


def generate(opts):
    options = opts.get("options", {})
    n = int(options['n'])
    m = int(options['m'])
    length = int(options.get('length', 1))
    bond = float(options.get('bond', 1.42))
    symbol = options.get('symbol', 'C')

    atoms = ase_nanotube(n, m, length=length, bond=bond, symbol=symbol)

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
