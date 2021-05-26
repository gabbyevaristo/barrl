# Barrl
Python Flask App for Controlling Automatic Bartending Robot

## Google Docs
A repository of project related content including presentations, reports, schedules, images, and videos can be found [here](https://drive.google.com/drive/u/1/folders/1snSKSgJmyOvtk9PzmkVpTZoNSdSPx8OJ).

## To set up a Barrl environment
- Clone the repository
- Using a virtual environment is recommended but not essential (skip if you are not using one)
  - In your terminal, run "pip install virtualenv"
  - In your terminal, run "virtualenv venv"
  - In your terminal, run "venv\\scripts\\activate" to activate the virtual environment
- In your terminal, run "pip install -r requirements.txt"

## To run the instance locally
- In your terminal, run "flask run"

## To run the instance on a Barrl Pi in production
- ssh into the local Raspberry Pi
- In your terminal, run "flask run --host=0.0.0.0"
