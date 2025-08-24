from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import List, Dict, Annotated, Optional, Literal
import pandas as pd
import pickle

with open("model.pkl", "rb") as f:
    model =  pickle.load(f)

app = FastAPI()



tier1Cities = [
    "Bangalore",
    "Chennai", 
    "Delhi",
    "Hyderabad",
    "Kolkata",
    "Mumbai",
    "Ahmedabad",
    "Pune"
]

tier2Cities = [
    "Agra", "Aligarh", "Allahabad", "Amravati", "Amritsar", "Asansol", 
    "Aurangabad", "Bareilly", "Belgaum", "Bellary", "Bhavnagar", "Bhopal", 
    "Bhubaneswar", "Bhiwandi", "Bikaner", "Bokaro Steel City", "Chandigarh", 
    "Coimbatore", "Cuttack", "Dehradun", "Dewas", "Dhanbad", "Durg-Bhilai", 
    "Faridabad", "Guntur", "Gurugram", "Guwahati", "Gwalior", "Hubli-Dharwad", 
    "Indore", "Jabalpur", "Jaipur", "Jalandhar", "Jamnagar", "Jamshedpur", 
    "Jammu", "Jodhpur", "Kanpur", "Karnal", "Kochi", "Kolhapur", 
    "Kozhikode", "Kota", "Lucknow", "Ludhiana", "Madurai", "Mangalore", 
    "Meerut", "Moradabad", "Mysore", "Nagpur", "Nashik", "Navi Mumbai", 
    "Nellore", "Noida", "Patna", "Pondicherry", "Pune", "Raipur", 
    "Rajkot", "Ranchi", "Ratlam", "Rewa", "Sagar", "Salem", "Satna", 
    "Shimla", "Shimoga", "Solapur", "Srinagar", "Surat", "Thane", 
    "Thiruvananthapuram", "Tiruchirappalli", "Tirupati", "Tiruppur", 
    "Ujjain", "Vadodara", "Varanasi", "Vasai-Virar", "Vellore", 
    "Vijayawada", "Visakhapatnam", "Warangal"
]

class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0,lt=120, description="Age of the User")]
    weight: Annotated[float, Field(...,gt=0,lt=200, description="Weight of the User in KGs")]
    height: Annotated[float, Field(...,gt=0,lt=2.5, description="Height of the User in Metres")]
    income_lpa: Annotated[float, Field(...,gt=0, description="Annual Salary of the User in Lakhs")]
    smoker: Annotated[bool, Field(...,description="Does the User Smoke?")]
    city: Annotated[str, Field(...,description="City of the User")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...,description="Occupation of the User")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi>30:
            return "high"
        elif self.smoker and self.bmi>25:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age<25:
            return "young"
        elif self.age<45:
            return "intermediate"
        elif self.age<60:
            return "middle aged"
        else:
            return "senior citizen"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier1Cities:
            return 1
        elif self.city in tier2Cities:
            return 2
        else:
            return 3
        


@app.get("/")
def home():
    return {"message":"Insurance Category Predictor"}

@app.post('/predict')
def predictPremium(data: UserInput):
    inputDF = pd.DataFrame([{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation,
        'city_tier':data.city_tier
    }])
    
    prediction = model.predict(inputDF)
    prediction = prediction[0]
    
    return JSONResponse(status_code=200,content={'predicted_category':prediction})