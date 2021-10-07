from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_db.db"
db = SQLAlchemy(app)
