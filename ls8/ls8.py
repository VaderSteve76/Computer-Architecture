#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


file_to_open = sys.argv[1]

print(f"Opening File: {file_to_open}")

file = open(file_to_open, "r")
instructions = []

for eachLine in file:
    if eachLine[0] != '#':
        if eachLine != '\n':
            instructions.append(int(eachLine[:8], 2))


cpu = CPU()

cpu.load(instructions)
cpu.run()
