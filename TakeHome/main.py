# -*- coding: utf-8 -*-
"""
Spyder Editor
@Author Prithvi Poddar 
This is a temporary script file.
"""


import io
from flask import Flask, flash, request, redirect, render_template ,url_for
import pandas as pd



app = Flask(__name__)
app.secret_key = b'2#456qwer'

# Check file type forCSV
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
           
#Rendering UI page for file upload 
@app.route('/')
def home():           
    return render_template('display.html')


#Check the CSV validations post Update
@app.route('/checkCSV', methods=['POST'])
def upload_file():
    #Fetching the file from the request
    file = request.files['file']
    #if empty file uploaded
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    #wrong format uploaded
    if not allowed_file(file.filename):
        flash('This selected file is not a CSV')
        return redirect(url_for('home'))
    #read csv file 
    if file:
       # Using input stream from io read the csv file 
       #set decoding to utf8 format
        inpStreamFile = io.StringIO(file.stream.read().decode("UTF8"))
        csvData= pd.read_csv(inpStreamFile)
        #Check for 10 rows and 3 columns 
        if csvData.shape[0]!=10 and csvData.shape[1]!=3:
            flash('The csv file does not have the required dimesions')
            return redirect(url_for('home'))
        #Check if the data has a null value and is incomplete csv
        if csvData.isnull().values.any():
            flash('The csv is not complete')
            return redirect(url_for('home'))
        
        flash('The Uploaded CSV is a valid CSV file')
        return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=80)



