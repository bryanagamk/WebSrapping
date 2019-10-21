import os

from flask import Flask
from flask import render_template
from flask import request
import logging as logger

logger.basicConfig(level="DEBUG")

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
engine = "mysql+pymysql://root:@localhost/flaskapp?host=localhost?port=3306"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = engine

db = SQLAlchemy(app)

if __name__ == "__main__":
    from api import *
    logger.debug("Starting Flask Server")
    app.run(debug=True, use_reloader=True)
