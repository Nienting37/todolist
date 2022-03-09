from flask import Flask
from microblog.devconfig import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
