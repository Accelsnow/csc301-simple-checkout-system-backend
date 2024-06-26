import os

basedir = os.path.abspath(os.path.dirname(__file__))

if 'RDS_HOSTNAME' in os.environ:
    db_uri = "mysql+pymysql://{}:{}@{}/{}".format(os.environ['RDS_USERNAME'], os.environ['RDS_PASSWORD'],
                                                  os.environ['RDS_HOSTNAME'], os.environ['RDS_DB_NAME'])
else:
    db_uri = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "9812(*&!@OIFdafdsafaljk"
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_SECURE = False
