import re
from flask import Flask, app, render_template, request

import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods = ['GET])
def Home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        year = int(request.form['Year'])
        present_price = float(request.form['Present_Price'])
        kms_driven = int(request.form['Kms_Driven'])
        kms_driven2 = np.log(kms_driven)
        owner = request.form['Owner']
        fuel_type = request.form['Fuel_Type']
        if(fuel_type == 'Petrol'):
            fuel_type = 1
            fuel_type_diesel = 0
        else:
            fuel_type = 0
            fuel_type_diesel = 1
        year = 2020 - year

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if (Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if(Transmission_Mannual == 'Manual Car'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
# Present_Price  Kms_Driven  Owner  no_year  Fuel_Type_Diesel  Fuel_Type_Petrol  Seller_Type_Individual  Transmission_Manual

        prediction = model.predict([[present_price, kms_driven2, owner, year,
                                   fuel_type_diesel, fuel_type, Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('result.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

    # return str(fuel_type)
    # return render_template("index.html", pp='Predicted Premium should be {}'.format(premium_predicted))


if __name__ == "__main__":
    app.run(debug=True)
