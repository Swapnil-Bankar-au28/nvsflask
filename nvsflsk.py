# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 19:34:06 2023

@author: dell
"""
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)
        df['Gender'] = df['Gender'].replace({'Female': 0, 'Male': 1})
        df['Gender'] = pd.to_numeric(df['Gender'])
        df['duplicate_location'] = df.duplicated(subset=['Location'], keep=False)
    
        # Group data by 'Surveyor name' and calculate the number of duplicate locations
        result = df.groupby('Surveyor name')['duplicate_location'].sum().reset_index()
        result.columns = ['Surveyor name', 'DUPLICATE LOCATION']
    
        # Merge the result with the original DataFrame
        result = pd.merge(result, df, on='Surveyor name')
    
        # Merge the result with the original DataFrame
    
    
        # Group data by 'Surveyor name' and calculate various statistics
        result =result.groupby('Surveyor name').agg({
            'Audio Duration (in secs)': ['count', 'sum'],
            'duplicate_location':['sum'],
           'Gender': ['count', 'sum'],
            'Timestamp': ['min', 'max'],
        }).reset_index()
    
        result['NO OF SAMPLES'] = result['Audio Duration (in secs)']['count'] - result['duplicate_location']['sum']#ivot_table = result.pivot_table(values='Gender', index='Surveyor name', aggfunc='count')
        # Rename columns
        #result.columns = ['EMPLOYEE NAME', 'NO OF SAMPLES', 'DURATION','DUPLICATE LOCATION', 'MALE', 'FEMALE', 'STARING TIME', 'ENDING TIME']
        result.columns = ['EMPLOYEE NAME', 'NO OF SAMPLES', 'DURATION', 'DUPLICATE LOCATION', 'FEMALE', 'MALE', 'STARING TIME', 'ENDING TIME', 'NEW COLUMN']
    
        # Calculate percentage of Male and Female
    
        result['MALE'] = (result['MALE'] / result['NO OF SAMPLES']) * 100
        result['FEMALE'] = (result['FEMALE'] / result['NO OF SAMPLES']) * 100
    
        result['FEMALE']= result['FEMALE']-result['MALE']
    
    
    
        # Convert 'STARING TIME' and 'ENDING TIME' columns to datetime
        result['STARING TIME'] = pd.to_datetime(result['STARING TIME'])
        result['ENDING TIME'] = pd.to_datetime(result['ENDING TIME'])
    
        # Add new column 'DURATION'
        result['DURATION'] = result['ENDING TIME'] - result['STARING TIME']
        result['DURATION'] = result['DURATION'].apply(lambda x: divmod(x.seconds, 3600))
        result['DURATION'] = result['DURATION'].apply(lambda x: f"{x[0]:0>2}:{x[1]//60:0>2}:{x[1]%60:0>2}")
        #result['DURATION'] = result['DURATION'].dt.total_seconds().div(60).round(2)
        #result['DURATION'] = result['DURATION'].div(60).round(2)
        # Print the result
        print(result)
        result.to_excel(r"C:\Users\dell\Downloads\swapnil_New.xlsx", index=False)
        
    
      
    
        return 'File uploaded and processed.'
    return '''
   <!doctype html>
    <title>Upload an Excel file</title>
    <h1>Upload an Excel file</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
if __name__ == '__main__':
    app.run()