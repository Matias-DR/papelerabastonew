#!/bin/bash

./bu.sh
git pull pa main
if [ $# -eq 0 ]
then
	python3 papelerabasto.py
fi
