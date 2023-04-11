import math
import string


def drinkingFormula():

    kg_or_lbs = input("Do you want to use kg or lbs? ")

    if kg_or_lbs == "kg":
        weight = int(input("Please enter your weight in kg "))
        print("You should drink a minimum of " + str(round((weight * 0.5 * 0.0295735296 * 2.20462262185),1)) + " liters of water to stay healthy")
    elif kg_or_lbs == "lbs":
        weight = int(input("Please enter your weight in lbs "))
        print("You should drink a minimum of " + str(weight * 0.5) + " oz to stay healthy")





if __name__ == '__main__':
    drinkingFormula()

