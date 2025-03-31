from flask import Flask, render_template, request
import pickle as pkl
import pandas as pd

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/details')
def details():
    return render_template('details.html')

def bin_age(age):
    age = int(age) # Ensure age is an integer
    if age < 10: return 1
    elif age < 20: return 2
    elif age < 30: return 3 
    elif age < 40: return 4
    elif age < 50: return 5
    elif age < 60: return 6
    elif age < 70: return 7
    elif age < 80: return 8
    elif age < 90: return 9
    else: return 10 # For ages 90 and above

def bin_hours(hours):
    hours = int(hours) # Ensure hours is an integer
    if hours < 10: return 2
    elif hours < 20: return 2
    elif hours < 30: return 3
    elif hours < 40: return 4
    elif hours < 50: return 5
    elif hours < 60: return 6
    elif hours < 70: return 7
    elif hours < 80: return 8
    elif hours < 90: return 9
    else: return 10

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve form data
        age = request.form.get('age')
        gender = request.form.get('gender')
        marital_status = request.form.get('marital_status')
        occupation=request.form.get('occupation')
        hours_per_week = request.form.get('hours_per_week')
        workclass = request.form.get('workclass')
        capital_gain = request.form.get('capital_gain')
        country = request.form.get('country')
        education = request.form.get('education')

        # Validate the data (you can add more robust validation here)
        if not all([age, gender, marital_status,occupation, hours_per_week, workclass, capital_gain, country, education])  :
            return render_template('details.html', error="Please fill in all fields.")
        
        age = bin_age(int(request.form.get('age')))
        hours_per_week = bin_hours(int(request.form.get('hours_per_week')))
        
        input_data = pd.DataFrame({
            'age': [age],
            'gender': [gender],
            'marital_status': [marital_status],
            'occupation':[occupation],
            'hours_per_week': [hours_per_week],
            'workclass': [workclass],
            'capital_gain': [capital_gain],
            'country': [country],
            'education': [education]
        })
        model_path="adult_income_model.pkl"
        with open(model_path,'rb') as file:
            model=pkl.load(file)
        result=model.predict(input_data)
        if result==0:
            prediction_result="<=50000"
        else:
            prediction_result=">50000"

        return render_template('result.html', prediction=prediction_result)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/model')
def model():
    return render_template('model.html')

if __name__ == '__main__':
    app.run(debug=True)
