import math
import string
from datetime import timedelta
import sqlite3
from sqlite3 import Error

from flask import Flask, redirect, url_for, render_template, request,session
#from flask_session import Session
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

app.secret_key = "AyyLMAO"
app.permanent_session_lifetime = timedelta(minutes=5)

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column("name",db.String(100))
    weight = db.Column("weight", db.Integer(5))

    def __int__(self, name, weight):
        self.name = name
        self.weight = weight
'''


messages = [{'title': 'Welcome!',
             'content': 'Please input the measurements you want to use'}]


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session['water'] = float(request.form['input'])
        session['water_intake'] = drinkingFormula1(float(request.form['input']))
        return redirect(url_for("yourwaterintake"))
    else:
        return render_template("base.html")

@app.route("/waterintake", methods=["POST","GET"])
def yourwaterintake():
    if 'water_intake' in session:
        if request.method == "POST":
            return redirect("/")
        if request.method == "POST":
            if request.form['water_detractor']:
                session['water_intake'] = session['water_intake']-0.4


    water_intake = session['water_intake']
    return render_template('waterintake.html', water_intake=water_intake)


@app.route('/optimal')
def optimal():
    return render_template("information_about_water_intake.html")

'''
@app.route('/personal', methods=["POST","GET"])
def personal():
    weight = None
    if request.method == "POST":
        weight = request.form["weight"]

        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["name"] = found_user.name


        else:
            usr = users(user,"")
            db.session.add(usr)
            db.session.commit()

    return render_template("user.html", weight = weight)
'''


def getWeightmesurement():
    session["weight"] = request.form['weight']
    return request.form['weight']

def drinkingFormula1(weight):
    water1 = session['water']
    if "weight" in session:
        weight = session["weight"]
        water1 = session['water']
        if weight == "kg":
            water = round((water1 * 0.5 * 0.0295735296 * 2.20462262185), 1)
        else:
            water = (water1 * 0.5 * 0.029576)
        return water
    else:
        weight = getWeightmesurement()
        if weight == "kg":
            water = round((water1 * 0.5 * 0.0295735296 * 2.20462262185), 1)
        else:
            water = (water1 * 0.5 * 0.029576)
        return water


def database():       
    conn = None
    try:
        conn = sqlite3.connect("db.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def createTable(c):
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS Users (
                                        login text PRIMARY KEY,
                                        weight SMALLINT NOT NULL,
                                    ); """
        
    sql_create_history_table = """ CREATE TABLE IF NOT EXISTS History (
                                        login text,
                                        date DATE,
                                        water FLOAT(2),
                                        Foreign Key (login) references Users (login),
                                        Primary Key (login, date)
                                    ); """
    if c is not None:
        # create projects table
        c.execute(sql_create_user_table)
        c.execute(sql_create_history_table)
    else:
        print("Error! cannot create the database connection.")



if __name__ == '__main__':
    #drinkingFormula()
    #db.create_all()
    c = database()

    app.run(debug=True)

