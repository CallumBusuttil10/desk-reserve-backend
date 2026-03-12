# desk-reserve-backend
Backend for Desk Reserve application for Assignment 1 ESE.


## Getting ready for development #
Before you start, make sure you do not have a VPN restricting access to the backend.

### Activate virtual environment ###
`source venv/bin/activate`

### Install requirements ###
`pip install -r requirements.txt`

### Migrate database ###
`python manage.py migrate`

### Create superuser ###
`python manage.py createsuperuser`

### Run server ###
`python manage.py runserver`

### Access admin panel ###
`http://localhost:8000/admin`