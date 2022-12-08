from flask import Flask
from app.config import ProductionConfig, DevelopConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(
    DevelopConfig
)  # or  app.config.from_object(ProductionConfig) if prod
db = SQLAlchemy(app)
migrate = Migrate(app, db)
client = app.test_client()
with app.app_context():
    from .commands import *

from app import routes, models
