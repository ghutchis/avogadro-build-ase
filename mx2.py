"""
/******************************************************************************
  This source file is part of the Avogadro project.
  This source code is released under the New BSD License, (the "License").
******************************************************************************/
"""

import argparse
import json
import sys
import os
import tempfile

import ase.io
from ase.build import mx2


def getOptions():
    userOptions = {}

    userOptions['a'] = {}
    userOptions['a']['type'] = 'integer'
    userOptions['a']['label'] = 'Width'
    userOptions['a']['minimum'] = 1
    userOptions['a']['default'] = 3

    userOptions['b'] = {}
    userOptions['b']['type'] = 'integer'
    userOptions['b']['label'] = 'Length'
    userOptions['b']['minimum'] = 1
    userOptions['b']['default'] = 3

    userOptions['c'] = {}
    userOptions['c']['type'] = 'integer'
    userOptions['c']['label'] = 'Layers'
    userOptions['c']['minimum'] = 1
    userOptions['c']['default'] = 1

    userOptions['kind'] = {}
    userOptions['kind']['label'] = 'Kind'
    userOptions['kind']['type'] = 'stringList'
    userOptions['kind']['default'] = 0
    userOptions['kind']['values'] = \
        ['2H', '1T']

    userOptions['metal'] = {}
    userOptions['metal']['label'] = 'Metal'
    userOptions['metal']['type'] = 'stringList'
    userOptions['metal']['default'] = 0
    userOptions['metal']['values'] = \
        ['Mo', 'W']

    userOptions['s'] = {}
    userOptions['s']['label'] = 'Anion'
    userOptions['s']['type'] = 'stringList'
    userOptions['s']['default'] = 0
    userOptions['s']['values'] = \
        ['S', 'Se', 'Te']

    opts = {'userOptions': userOptions}

    return opts


def generate(opts):
    a = int(opts['a'])
    b = int(opts['b'])
    c = int(opts['c'])
    metal = opts['metal']
    s = opts['s']
    type = f"{metal}{s}2"

    atoms = mx2(type, opts['kind'], size=(a,b,c))

    # secure tempfile name ending in ".xyz" in a writable tmpdir
    fd, name = tempfile.mkstemp(".xyz")
    os.close(fd) # don't need the filehandle

    ase.io.write(name, atoms, format="xyz")

    with open(name) as f:
        xyzData = f.read()
    os.remove(name)

    return xyzData


def runCommand():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Append tube in xyz format (Avogadro will bond everything)
    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = generate(opts)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Metal Dichalcogenide')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Metal Dichalcogenide...")
    if args['menu_path']:
        print("&Build|Insert")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
