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
from random import randrange

import ase.io
from ase.build import graphene_nanoribbon


def getOptions():
    userOptions = {}

    userOptions['n'] = {}
    userOptions['n']['type'] = 'integer'
    userOptions['n']['default'] = 1

    userOptions['m'] = {}
    userOptions['m']['type'] = 'integer'
    userOptions['m']['default'] = 1

    userOptions['type'] = {}
    userOptions['type']['label'] = 'Type'
    userOptions['type']['type'] = 'stringList'
    userOptions['type']['default'] = 0
    userOptions['type']['values'] = \
        ['Armchair', 'Zigzag']


    opts = {'userOptions': userOptions}

    return opts


def generate(opts):
    m = int(opts['m'])
    n = int(opts['n'])
    type = 'armchair'
    if 'zig' in opts['type']:
        type = 'zigzag'

    atoms = graphene_nanoribbon(n, m, type)
    # need a better random temporary name
    name = 'temp{}.xyz'.format(randrange(32768))
    ase.io.write(name, atoms, format="xyz")

    with open(name) as f:
        xyzData = f.read()
    #os.remove(name)

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
    parser = argparse.ArgumentParser('Nanoribbon')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Nanoribbon...")
    if args['menu_path']:
        print("&Build|Insert")
    if args['print_options']:
        print(json.dumps(getOptions()))
    elif args['run_command']:
        print(json.dumps(runCommand()))
