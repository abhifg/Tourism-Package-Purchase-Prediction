from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('https://raw.githubusercontent.com/Suvam-Bit/Datasets/main/Tourism%20Package%20Purchase%20Prediction/over_sampled.csv')
X = df.drop('ProdTaken', axis = 1)
y = df['ProdTaken']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

app = Flask(__name__, template_folder='templates')
model = pickle.load(open('knn_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = float(request.form['age'])**(1/2)

        city_tier = float(request.form['city_tier'])

        dur_of_pitch = float(request.form['dur_of_pitch'])**(1/5)

        num_of_persons_vis = float(request.form['num_of_persons_vis'])

        num_of_followups = float(request.form['num_of_followups'])
        
        pref_prop_star = float(request.form['pref_prop_star'])

        num_of_trips = float(request.form['num_of_trips'])

        passport = float(request.form['passport'])

        pitch_sat_score = float(request.form['pitch_sat_score'])

        own_car = float(request.form['own_car'])

        num_of_child_vis = float(request.form['num_of_child_vis'])

        monthly_income = np.log(float(request.form['monthly_income']))

        self_enquiry = 0

        large_business = 0
        salaried = 0
        small_business = 0

        male = 0

        delux = 0
        king = 0
        standard = 0
        super_delux = 0

        married = 0
        single = 0

        executive = 0
        manager = 0
        senior_manager = 0
        vp = 0
        
        type_of_contact = request.form['type_of_contact']
        if type_of_contact == 'self_enquiry':
            self_enquiry = 1
        
        occupation = request.form['occupation']
        if occupation == 'large_business':
            large_business = 1
        elif occupation == 'salaried':
            salaried = 1
        elif occupation == 'small_business':
            small_business = 1

        gender = request.form['gender']
        if gender == 'male':
            male = 1
        
        prod_pitched = request.form['prod_pitched']
        if prod_pitched == 'delux':
            delux = 1
        elif prod_pitched == 'king':
            king = 1
        elif prod_pitched == 'standard':
            standard = 1
        elif prod_pitched == 'super_delux':
            super_delux = 1
        
        marital_status = request.form['marital_status']
        if marital_status == 'married':
            married = 1
        elif marital_status == 'single':
            single = 1

        designation = request.form['designation']
        if designation == 'executive':
            executive = 1
        elif designation == 'manager':
            manager = 1
        elif designation == 'senior_manager':
            senior_manager = 1
        elif designation == 'vp':
            vp = 1

        input = scaler.transform([[age,
                                    city_tier,
                                    dur_of_pitch,
                                    num_of_persons_vis,
                                    num_of_followups,
                                    pref_prop_star,
                                    num_of_trips,
                                    passport,
                                    pitch_sat_score,
                                    own_car,
                                    num_of_child_vis,
                                    monthly_income,
                                    self_enquiry,
                                    large_business,
                                    salaried,
                                    small_business,
                                    male,
                                    delux,
                                    king,
                                    standard,
                                    super_delux,
                                    married,
                                    single,
                                    executive,
                                    manager,
                                    senior_manager,
                                    vp]])

        prediction = model.predict(input)

        if prediction[0] == 1:
            return render_template('predictor.html',prediction_text="Go ahead! The customer will going to buy the tourism package!")
        else:
            return render_template('predictor.html',prediction_text="Oops! The customer will not going to buy the tourism package!")
    
    else:
        return render_template('index.html')
    
if __name__=="__main__":
    app.run(debug=True)