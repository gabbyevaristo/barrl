# barrl
Python Flask App for Controlling Automatic Bartending Robot

## Google Docs
A repository of project related content including presentations, reports, schedules, images, and videos can be found [here](https://drive.google.com/drive/u/1/folders/1snSKSgJmyOvtk9PzmkVpTZoNSdSPx8OJ).

## To set up a Barrl environment
- clone the repository
- using a virtual environment is recommended but not essential (skip if not using one)
  - in your terminal run "pip install virtualenv"
  - in your terminal run "virtualenv venv"
  - in your terminal run "venv\\scripts\\activate" to activate the virtual environment
- in your terminal run "pip install -r requirements.txt"

## To Run the instance Locally
- in your terminal run "flask run"

## To Run the instance on a Barrl Pi in Production
- ssh into the local raspberry pi
- in your terminal, run "flask run hostname=0.0.0.0"
