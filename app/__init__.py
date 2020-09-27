from flask import Flask
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from serializable import Serializable


class CheckoutJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Serializable):
            return o.serialize(recur=0)

        return super(CheckoutJSONEncoder, self).default(o)


app = Flask(__name__)
CORS(app=app, supports_credentials=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.json_encoder = CheckoutJSONEncoder

from app import routes
