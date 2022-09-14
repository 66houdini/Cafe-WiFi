from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

uri = os.getenv("DATABASE_URL", "sqlite:///cafes.db")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "sgdhsjfdu")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///cafes.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)
db = SQLAlchemy(app)
Bootstrap(app)
db.Model.metadata.reflect(db.engine)


class CafeList(db.Model):
    __table__ = db.Model.metadata.tables["cafe"]

    def __repr__(self):
        return self.name


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes_list():
    cafes = CafeList.query.all()
    return render_template("cafes.html", cafes=cafes)


if __name__ == "__main__":
    app.run(debug=True)
