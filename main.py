import datetime
import math
import string
from datetime import timedelta


from flask import Flask, redirect, url_for, render_template, request,session,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm

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
    if 'weight' in session:
        
        session['water_intake'] = drinkingFormula1(float(getWeightmesurement()))
        return(url_for("yourwaterintake"))
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


@app.route('/personal/<id>', methods=["POST","GET"])
def personal():
    if request.method == "POST":
        name = db.get_or_404(User, id)
        found_user = User.query.filter_by(id = login).first()
        if found_user:
            session["name"] = found_user.name

        else:
            usr = User(id,"")
            db.session.add(usr)
            db.session.commit()

    return render_template("user.html", weight = name)



def getWeightmesurement():
    #session['weight'] = request.form['weight']
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

@app.route("/register",methods=["POST","GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect((url_for('/')))

    return render_template('register.html', title='Register', form =form)

@app.route("/login")
def login1():
    form = LoginForm()
    return render_template('login.html', title='Login', form =form)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    lbs_or_kg = db.Column(db.String(20),unique=True,nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
class History(db.Model):
    id = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    waterIntake = db.Column(db.Float)
    waterGoal = db.Column(db.Float)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

