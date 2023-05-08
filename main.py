import datetime
import math
import string
from datetime import timedelta


from flask import Flask, redirect, url_for, render_template, request,session,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, CalculatorForm

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"
db.init_app(app)
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

app.secret_key = "AyyLMAO"
app.permanent_session_lifetime = timedelta(minutes=5)




messages = [{'title': 'Welcome!',
             'content': 'Please input the measurements you want to use'}]


@app.route("/")
def welcomepage():
    return render_template("welcome.html")

@app.route("/calculator", methods=["POST", "GET"])
def calculator():
    form = CalculatorForm()
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


@app.route('/personal/<user>', methods=["POST","GET"])
def personal(user):
    if request.method == "POST":
        name = db.get_or_404(User, id)
        found_user = User.query.filter_by(id = user).first()
        if found_user:
            session["name"] = found_user.name

        else:
            usr = User(id,"")
            db.session.add(usr)
            db.session.commit()

    return render_template("user.html", weight = name)

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect((url_for('/')))

    return render_template('register.html', title='Register', form =form)

@app.route("/login",methods=["POST","GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit:
            user = User.query.filter(User.username == form.username, User.password == form.password).first()
            if not user:
              return render_template('register.html', title='Register', form =form)
            else:
                return render_template('personal/<user>', user = user.username)
    else:
        return render_template('login.html', title='login', form=form)


class User(db.Model):
    username = db.Column(db.String(20), unique=True,nullable=False, primary_key=True)
    lbs_or_kg = db.Column(db.String(20),unique=True,nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class History(db.Model):
    user = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    waterIntake = db.Column(db.Float)
    waterGoal = db.Column(db.Float)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

