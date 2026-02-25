"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import os
import tempfile

import ase.io
from ase.build import graphene_nanoribbon


def generate(opts):
    options = opts.get("options", {})
    m = int(options['m'])
    n = int(options['n'])
    ribbon_type = 'zigzag' if 'zig' in options['type'].lower() else 'armchair'

    atoms = graphene_nanoribbon(n, m, ribbon_type)

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
