"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import os
import tempfile

import numpy as np
import spglib
import ase.io
from ase import Atoms
from ase.build import surface
from ase.cell import Cell


def cjson_to_atoms(cjson):
    coords = list(cjson["atoms"]["coords"]["3d"])
    numbers = list(cjson["atoms"]["elements"]["number"])

    positions = np.array(coords).reshape(-1, 3)

    atoms = Atoms(numbers=numbers, positions=positions)

    if "unitCell" in cjson:
        uc = cjson["unitCell"]
        cell = Cell.fromcellpar([
            uc["a"], uc["b"], uc["c"],
            uc["alpha"], uc["beta"], uc["gamma"],
        ])
        atoms.set_cell(cell)
        atoms.set_pbc(True)

    return atoms


def generate(opts):
    cjson = opts.get("cjson", {})
    options = opts.get("options", {})

    atoms = cjson_to_atoms(cjson)

    # Reduce to primitive cell before surface construction
    spglib_cell = (atoms.get_cell(), atoms.get_scaled_positions(), atoms.get_atomic_numbers())
    primitive = spglib.find_primitive(spglib_cell, symprec=1e-5)
    if primitive is not None:
        lattice, scaled_positions, numbers = primitive
        atoms = Atoms(numbers=numbers, scaled_positions=scaled_positions, cell=lattice, pbc=True)

    h = int(options.get("h", 1))
    k = int(options.get("k", 0))
    l = int(options.get("l", 0))
    layers = int(options.get("layers", 4))
    vacuum = float(options.get("vacuum", 10.0))

    slab = surface(atoms, (h, k, l), layers, vacuum=vacuum)
    # Ensure all three lattice vectors are present in the extxyz output
    slab.set_pbc(True)

    fd, name = tempfile.mkstemp(".xyz")
    os.close(fd)

    ase.io.write(name, slab, format="extxyz")

    with open(name) as f:
        xyz_data = f.read()
    os.remove(name)

    return xyz_data


def run(avo_input):
    return {
        'moleculeFormat': 'xyz',
        'xyz': generate(avo_input),
    }
