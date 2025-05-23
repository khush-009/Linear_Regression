from flask import Flask,render_template,request,jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app = application

# import ridge regressor and standard scaler pickle
ridge_model = pickle.load(open('models/ridgereg.pkl','rb'))
standard_scaler_model = pickle.load(open('models/scaler.pkl','rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict",methods=['GET','POST'])
def predict_data():
    if request.method=="POST":
        Temperature = float(request.form.get('Temperature'))
        RH = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        ISI = float(request.form.get('ISI'))
        Region = float(request.form.get('Region'))

        new_data_scaled = standard_scaler_model.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Region]])
        result = ridge_model.predict(new_data_scaled)

        return render_template('home.html',results=result[0])

    else:
        return render_template('home.html')

if __name__=='__main__':
    app.run(host="0.0.0.0")
