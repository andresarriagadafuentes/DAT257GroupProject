def drinkingFormula():
    weight = int(input("Please enter your weight in kg "))
    print("You should drink this amount in dl " + str(weight * 0.5 * 0.29574*2.20462262185))


if __name__ == "__main__":
    drinkingFormula()
