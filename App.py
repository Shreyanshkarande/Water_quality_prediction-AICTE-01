#import all the neccessary library 
import pandas as pd
import numpy as np 
import joblib
import pickle 
import streamlit as st

# load the model and structure 
model =joblib.load("pollution_model.pkl")
model_cols =joblib.load("model_columns.pkl")


#Let's create an User interface.
st.title("Water Pollutants Predictor")
st.write("Predict the water pollutants based on Year and Station ID")#1-22


#User inputs
year_input=st.number_input("Enter Year" , min_value=2000 ,  max_value=2100,value=2022)
station_id =st.text_input("Enter Station ID")

# to encode and predict 
if st.button('Predict'):
    if not station_id:
        st.warning('Pease enter the station ID')
    else:
        #prepare the input
        input_df =pd.DataFrame({'year':[year_input],'id':[station_id]})
        input_encoded = pd.get_dummies(input_df,columns=['id'])

        #Align with model cols 
        for col in model_cols:
            if col not in input_encoded:
                input_encoded[col]=0
        input_encoded=input_encoded[model_cols]

        #predicting 
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants =['O2', 'NO3', 'NO2', 'SO4','PO4', 'CL']

        st.subheader(f"Predicted pollutant levels for station '{station_id}' in {year_input}:")

        # Prepare table
        result_table = pd.DataFrame({
            'Pollutant': pollutants,
            'Predicted Value': [f"{val:.2f}" for val in predicted_pollutants]
        })

        st.table(result_table)