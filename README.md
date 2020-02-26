# SCTF Password Manager Server

# Development
To get started setup python3 and python3-virtualenv on your machine.

Run the following commands to setup your development environment
```bash
# Installatino & setup
sudo apt-get install python3 python3-virtualenv
python3 -m virtualenv venv

# Active it
. ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python3 manage.py makemigrations
python3 manage.py migrate

# Test server
python3 manage.py test

# Run Server
python3 manage.py runserver
```

# Deployment
Will be added later