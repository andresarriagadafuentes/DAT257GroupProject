import math
import string
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"









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

