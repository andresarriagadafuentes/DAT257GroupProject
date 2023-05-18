import math
import string
from datetime import timedelta

import flask_login
from flask import Flask, redirect, url_for, render_template, request,session,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, CalculatorForm
from flask_bcrypt import bcrypt
from flask_login import LoginManager,UserMixin,login_user, current_user, logout_user, login_required

user1 = current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager(app)

app.secret_key = "AyyLMAO"
app.permanent_session_lifetime = timedelta(minutes=5)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()

messages = [{'title': 'Welcome!',
             'content': 'Please input the measurements you want to use'}]


@app.route("/")
def welcomepage():
    return render_template("welcome.html")

@app.route("/calculator", methods=["POST", "GET"])
def calculator():
    form = CalculatorForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            user = flask_login.current_user
            form.lbs_or_kg.data = user.lbs_or_kg
            form.weight.data = user.weight
    if request.method == "POST":
        session['water_intake'] = drinkingFormula1(form.lbs_or_kg.data,form.weight.data,form.minutes_of_exercise.data)
        return redirect(url_for("yourwaterintake"))

    else:
        return render_template('base.html', title='WaterIntake', form=form)


@app.route("/waterintake", methods=["POST","GET"])
def yourwaterintake():
    
    water_intake = session['water_intake']
    return render_template('waterintake.html', water_intake=water_intake)


@app.route('/information_about_water_intake')
def optimal():
    return render_template("information_about_water_intake.html")




@app.route('/personal/', methods=["POST","GET"])
def personal():
    if current_user.is_authenticated:
        user = flask_login.current_user
        if request.method == "POST":
            name = request.form.get('name')
            weight = request.form.get('weight')
            password = request.form.get('password')
            user = User.query.get(name)
            if user:
                user.name = name
                user.weight = weight
                user.password = password
                db.session.commit()
        history = History.query.filter_by(user = user1.username).order_by(History.date.desc()).limit(7).all()
        return render_template("user.html", user = user1.username, water_intake_history = history)
    else:
        return redirect((url_for('login')))



@app.route('/RiskOfDying')
def RiskofDying():
    return render_template("RiskOfDying.html")

@app.route('/information')
def information():
    return render_template("information_page.html")

@app.route('/too_much_water')
def too_much_water():
    return render_template("too_much_water.html")

def getWeightmesurement():
    #session['weight'] = request.form['weight']
    return request.form['weight']

def drinkingFormula1(lbs_or_kg,weight,exercise):


    if lbs_or_kg.upper() == "KG":
        water = round((weight * 0.5 * 0.0295735296 * 2.20462262185), 1) + (exercise*0.01)
    else:
        water = (weight * 0.5 * 0.029576) + (exercise*0.0338)
    return water

@app.route("/register",methods=["POST","GET"])
def register():
    #if current_user.is_authenticated:
    #    return redirect(url_for("/calculator"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,lbs_or_kg=form.lbs_or_kg.data,weight=form.weight.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect((url_for('login')))
    return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=["POST","GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("personal"))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        password = form.password.data
        if user is not None:
            if password == user.password:
                login_user(user, remember=form.remember.data)
                user1 = user
                return redirect((url_for('welcomepage')))
            else:
                flash('Login Unsuccessful, please register a user with that name.')
        else:
            flash('Login Unsuccessful, please register a user with that name.')
    return render_template('login.html', title='login', form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect((url_for("welcomepage")))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    lbs_or_kg = db.Column(db.String(20),nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.lbs_or_kg}','{self.weight}','{self.password}')"




class History(db.Model):
    user = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    waterIntake = db.Column(db.Float)
    waterGoal = db.Column(db.Float)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

