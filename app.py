# for the first example code used ChatGPT, after a lot of manipulations manually

# check if all Libraries are installed
from libs.missingLibs import check
check()

# Datapreperation
import pandas as pd

#%% Import the model including ml modell, scaler and headers
# Load the saved model
import joblib
# the choosen ML Algorithm with the Benchmarks.
# Load the trained model and scaler
model = joblib.load('libs/model.pkl')  # Load the model
scaler = joblib.load('libs/scaler.pkl')  # Load the scaler object

# Read headers back from the text file
with open('libs/headers.txt', 'r') as f:
    headers = [line.strip() for line in f]  # Remove newline characters

# print(headers)  # Display the headers 

#%% Report generation

# Report generation
# set to 1 if you want to use the LLM
# report_llm = 0
# if report_llm: 
#     from libs.Report_generation import init_report_generation, generate_report
#     LLM_pipeline = init_report_generation()
# else:
from libs.Manual_Report import HealthReportGenerator
report_generator = HealthReportGenerator()

# from libs.LLM_check import init_LLM_check, check
# LLM_pipe_check = init_LLM_check()
# Build the Pipeline
from libs.LLM_check import TextRestructurer
# api_key = Secret.from_token("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")
api_key = "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"
restructurer = TextRestructurer(api_key)

import re
def clean_text(text):
    pattern = '|'.join(map(re.escape, ['<p>', '</p>', '<br>', ':', '\n']))
    return re.sub(pattern, '', text)

from libs.LLM_feedback import feedback
feedback_LLM = feedback(api_key)


#%% Risk cathegorisation

def categorize_risk(risk_probability):
    if risk_probability >= 0.6:
        return "High Risk"
    elif risk_probability >= 0.25:
        return "Elevated Risk"
    else:
        return "Low Risk"

#%% Create Logfile to check if the evaluation does the right thing
import csv
import time

# Define the log file
log_file = 'log/logfile.csv' 


# Function to log a message
def log_entry(data):
    # Get the current timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # Open the CSV file in append mode
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writerow(['Timestamp'] + list(data.columns))
        # Write the log entry
        writer.writerow([timestamp]+ data.iloc[0].to_list())

contact_file = 'log/contact.csv' 

# Function to log a message
def log_contact(data):
    # Get the current timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # Open the CSV file in append mode
    with open(contact_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writerow(['Timestamp'] + list(data.columns))
        # Write the log entry
        writer.writerow([timestamp]+ data.iloc[0].to_list())

    
#%% Flask Application

# Online application
from flask import Flask, render_template, request
from markupsafe import escape
import numpy as np

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    # Getting the form data
    df = request.form.to_dict()
    df = pd.DataFrame(df, index=[1])
    df.head()
    
    # Calculate BMI
    df['BMI'] = df['weight'].astype(float) / (df['height'].astype(float) / 100)**2
    df['currentSmoker'] = np.where(df['cigsPerDay'].astype(int) > 0, 1, 0)

    # Standardize Data (make sure you fit the scaler during training and just transform during prediction)
    # Use the previously fitted scaler (Assume it's saved or loaded from the model)
    X=  df[headers]
    X = scaler.transform(X)

    # Make prediction
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)
    
    # Extract the risk probability and categorize risk
    risk_probability = y_prob[0][1]
    risk_category = categorize_risk(risk_probability)
    
    text = report_generator.generate_report(df[headers].iloc[0].astype('int32').to_dict())
    text = str(text)
    df['manual_text'] = text.encode("cp1252", errors="replace").decode("utf-8")

    try:
        if df['data_processing'].notna().any():
            text = clean_text(text)
            text = restructurer.restructure_text(text)
            df['LLM_text'] = text.encode("cp1252", errors="replace").decode("utf-8")
            df = df.drop('data_processing', axis=1)
    except:
        pass

    # prepare log entry:
    df['ML-model'] = type(model).__name__
    df['Parameters'] = str(model.get_params()).encode("cp1252", errors="replace").decode("utf-8")
    df['proba'] = np.round(y_prob[0][1]*100,2)
    df['prediction'] = y_pred
    df.head()

    log_entry(df)

    return render_template('report.html',
                           text = text,
                        #    data = df.iloc[0].to_dict(),
                           patient_name= df['Name'][1],
                           age = df['age'][1],
                           gender = df['male'][1],
                           risk_level = risk_category,
                           TenYearCHD = y_pred)

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/agb")
def agb():
    return render_template('agb.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/terms")
def terms():
    return render_template('agb.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/submit_contact_form", methods=['POST'])
def submit_contact_form():
    df = request.form.to_dict()
    df = pd.DataFrame(df, index=[1])
    answer = feedback_LLM.give_feedback(df['message'][1])
    df['answer'] = answer
    log_contact(df)
    return render_template('submit_contact_form.html', answer = answer)

@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


from waitress import serve

# Run the Application
if __name__ == '__main__':
    # app.run(host = '192.168.1.36', debug=True)
    # app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000)
    serve(app, host='0.0.0.0', port=8000, threads=30)

