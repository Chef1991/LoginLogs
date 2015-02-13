#!/bin/bash

_script="$(readlink -f ${BASH_SOURCE[0]})"

## Delete last component from $_script ##
_base="$(dirname $_script)"

## Okay, print it ##
echo "Script name : $_script"
echo "Current working dir : $PWD"
echo "Script location path (dir) : $_base"