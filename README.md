# Barrl
Never wait for a bartender again

## Project Overview
Today, the process of getting an alcoholic drink at a bar or social event is a nightmare. There are crowds, risks of getting COVID, long lines, slow bartenders, payment risks, and expensive tips. Our team is undertaking a project to change that process so that customers can get a drink more easily, more quickly, contactlessly, safely, and more cheaply. We are going to achieve this by building Barrl, an automatic bartending system where users can order a drink, pay contactlessly, and have their drink poured automatically by our machine - no lines, no waiting, and no need to tip. Barrl units will consist of a secure wine barrel body to store the bottles and ingredients and a dispensing unit atop the device where a user can place their glass for a drink to be poured. In order to place an order, users need only connect to the local wifi of the venue, scan a QR code on Barrl to access its website, select their drink, pay, and watch as their drink is poured.

## Resources
A repository of project related content including presentations, literature review, reports, schedules, images, and videos can be found [here](https://drive.google.com/drive/u/1/folders/1snSKSgJmyOvtk9PzmkVpTZoNSdSPx8OJ).

## How to build a Barrl
An inventory of all the required hardware and the cost to build a Barrl unit can be found [here](https://docs.google.com/spreadsheets/u/1/d/1oeld_4YFFCOyfyVn-yoKrc7Vv1LyA8GUgOt9WdFAWWM/edit#gid=0).

## Required Software
To run a Barrl instance you will need:
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

## Long Term Goals
- Increase number of dispensable liquids
- Expand type of beverages served
- Cup dispenser
- Ice dispenser
- Refrigeration
- Empty ingredient bottle sensing
- Spill protection
- Manage & deploy multiple Barrl units at once

## Created By
- Ted Schelble ([@tschelbs18](https://github.com/tschelbs18))
- Gabrielle Evaristo ([@gabbyevaristo](https://github.com/gabbyevaristo))
- Erik Delanois ([@JEDelanois](https://github.com/@JEDelanois))
