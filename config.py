import os
from datetime import timedelta

# configuration
DEBUG = True
SECRET_KEY = 'this-is-a-secret-key'
TOKEN_EXPIRY = timedelta(days=1)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (
    os.environ.get('DBUSER'), os.environ.get('DBPASS'), os.environ.get('DBHOST'), os.environ.get('TODODB'))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
