import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Category Predictor")

st.markdown("Enter your details below")

#Input Fields
age = st.number_input("Age",min_value=1, max_value=120,value=30)
height = st.number_input("Height",min_value=0.5,max_value=2.5,value=1.78)
weight = st.number_input("Weight",min_value=1.0,value=65.0)
income_lpa =  st.number_input("Income in LPA",min_value=1.0,value=12.0)
smoker = st.selectbox("Are you a smoker?",options=["Yes","No"])
city = st.text_input("City",value="Mumbai")
occupation = st.selectbox("Occupation", options=['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'])

if st.button("Predict Premium Category"):
    input_data = {
        "age":age,
        "weight":weight,
        "height":height,
        "income_lpa":income_lpa,    
        "smoker":smoker,
        "city":city,
        "occupation":occupation
    }
    
    try:
        response = requests.post(API_URL,json=input_data)
        if response.status_code==200:
            result = response.json()
            st.success(f"Predicted Insurance Premium Category: **{result['response']['predicted_category']}**")
        else:
            st.error(f"API Error: {response.status_code}-{response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI Server.")