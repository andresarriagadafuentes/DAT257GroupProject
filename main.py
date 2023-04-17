import math
import string
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

messages = [{'title': 'Welcome!',
             'content': 'Please input the measurements you want to use'}]


    


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        water_intake = drinkingFormula1(float(request.form['input']))
        return render_template('waterintake.html', water_intake=water_intake)
    else:
        return render_template("base.html")

@app.route('/optimal')
def optimal():
    return render_template("information_about_water_intake.html")

def getWeightmesurement():
     return request.form['weight']

def drinkingFormula1(weight):
    if getWeightmesurement() == "kg":
        water = round((weight * 0.5 * 0.0295735296 * 2.20462262185), 1)
    else:
        water = (weight * 0.5 * 0.029576)
    return water





if __name__ == '__main__':
    #drinkingFormula()
    app.run(debug=True)

