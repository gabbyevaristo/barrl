# Barrl
Never wait for a bartender again

## How to build a Barrl
An inventory of all the required hardware and the cost to build a Barrl unit can be found [here.](https://docs.google.com/spreadsheets/u/1/d/1oeld_4YFFCOyfyVn-yoKrc7Vv1LyA8GUgOt9WdFAWWM/edit#gid=0).

## Required Software
To run a Barrl instance, you will need:
- [Python](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)

## To set up a Barrl environment
1. Clone the repository
2. Using a virtual environment is recommended but not essential (skip if you are not using one)
  1. In your terminal, run "pip install virtualenv"
  2. In your terminal, run "virtualenv venv"
  3. In your terminal, run "venv\\scripts\\activate" to activate the virtual environment
3. In your terminal, run "pip install -r requirements.txt"

## To run the instance locally
1. In your terminal, run "flask run"

## To run the instance on a Barrl Pi in production
1. ssh into the local Raspberry Pi
2. In your terminal, run "flask run --host=0.0.0.0"

## Created By
- Erik Delanois ([@JEDelanois](https://github.com/@JEDelanois))
- Gabrielle Evaristo ([@gabbyevaristo](https://github.com/gabbyevaristo))
- Ted Schelble ([@tschelbs18](https://github.com/tschelbs18))
