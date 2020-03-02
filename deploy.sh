# Pull repository

git clone git@github.com:TarikvdBerg/project-homeland.git

# Set environment
setenv HOMELAND_DEBUG False

# Goto project
cd project-homeland

# Install dependencies
pip install -r requirements.txt

# Start django application
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver 0.0.0.0:80 &