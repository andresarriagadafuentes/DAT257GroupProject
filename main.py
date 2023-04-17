import math
import string
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

messages = [{'title': 'Welcome!',
             'content': 'Please input the measurements you want to use'}]

@app.route('/')
def index():
    return render_template('messages.html', messages=messages)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        water_intake = drinkingFormula1(request.form['nm'])
        return render_template('waterintake.html', water_intake=water_intake)
    else:
        return render_template("information_about_water_intake.html")

@app.route('/optimal')
def optimal():
    return render_template("information_about_water_intake.html")

def getWeightmesurement():
     return request.form['weight']

def drinkingFormula1(weight):
    if getWeightmesurement() == "kg":
        water = round((weight * 0.5 * 0.0295735296 * 2.20462262185), 1)
    else:
        water = (weight * 0.5)
    return water


def drinkingFormula():

    kg_or_lbs = input("Do you want to use kg or lbs? ")

    if kg_or_lbs == "kg":
        weight = int(input("Please enter your weight in kg "))
        print("You should drink a minimum of " + str(round((weight * 0.5 * 0.0295735296 * 2.20462262185),1)) + " liters of water to stay healthy")
    elif kg_or_lbs == "lbs":
        weight = int(input("Please enter your weight in lbs "))
        print("You should drink a minimum of " + str(weight * 0.5) + " oz to stay healthy")





if __name__ == '__main__':
    #drinkingFormula()
    app.run(debug=True)

