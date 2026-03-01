#!/bin/bash

set -e  # Exit immediately if a command fails

VENV=".venv"

echo "-------- Detecting Python version --------"
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version detected: $PYTHON_VERSION"

echo "-------- Checking if running on Ubuntu --------"
if grep -qi ubuntu /etc/os-release; then
    echo "Ubuntu detected"

    echo "-------- Updating package list --------"
    sudo apt update

    echo "-------- Installing python$PYTHON_VERSION-venv --------"
    sudo apt install -y python$PYTHON_VERSION-venv
fi

echo "-------- Creating virtual environment --------"
python3 -m venv $VENV

echo "-------- Activating virtual environment --------"
source $VENV/bin/activate
echo "Virtual environment activated"

echo "-------- Upgrading pip --------"
pip install --upgrade pip

echo "-------- Installing dependencies --------"
pip install -r requirements.txt

echo "-------- Running Django migrations --------"
python manage.py makemigrations --noinput
python manage.py makemigrations home --noinput
python manage.py migrate --noinput

# echo "-------- Collecting static files --------"
# python manage.py collectstatic --noinput

echo "-------- ready to be deployed --------"