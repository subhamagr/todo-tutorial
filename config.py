import os

# configuration
DEBUG = True
SECRET_KEY = 'this-is-a-secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (
    os.environ.get('DBUSER'), os.environ.get('DBPASS'), os.environ.get('DBHOST'), os.environ.get('TODODB'))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
