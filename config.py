import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
Use environment variable
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'temi_')
DB_PASSWORD = os.getenv('DB_PASSWORD', '08068866823')
DB_NAME = os.getenv('DB_NAME', 'fyyur')

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://temi_:08068866823@localhost:5432/fyyurapp'
