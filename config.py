import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

if os.environ['RDS_HOSTNAME']:
    db_uri = "mysql://{}:{}@{}/{}".format(os.environ['RDS_USERNAME'], os.environ['RDS_PASSWORD'],
                                          os.environ['RDS_HOSTNAME'], os.environ['RDS_DBNAME'])
else:
    db_uri = 'sqlite:///' + os.path.join(basedir, 'app.db')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "*(*@!^sdafl318"
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
