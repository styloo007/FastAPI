from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, AnyUrl, computed_field, field_serializer, model_serializer
from typing import List, Dict, Optional, Annotated, Literal
import json

app =  FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the Patient",examples=['P001'])]
    name : Annotated[str, Field(..., description='Name of the Patient', examples=['John Doe'])]
    city : Annotated[str, Field(..., description='City where the patient resides in', examples=['Bangalore, Delhi'])]
    age: Annotated[int, Field(..., description='Age of the Patient', gt=0, lt=150, examples=[45,22])]
    gender: Annotated[Literal['male','female','others'], Field(..., description='Gender of the Patient')]
    height: Annotated[float, Field(..., description='Height of the Patient in Metres', gt=0)]
    weight: Annotated[float, Field(..., description='Weight of the Patient in KGs', gt=0, lt=150)]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2))
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'underweight'
        elif self.bmi<25:
            return 'normal'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'
    
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male','female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None,gt=0)]
    

def loadPatientData():
    with open('patientsData.json', 'r') as f:
        data = json.load(f)
    return data

def saveData(data):
    with open('patientsData.json', 'w') as f:
        json.dump(data,f)

@app.get("/")
def home():
    return {'message':'Patitent Management System API'}

@app.get("/about")
def about():
    return {'message':'A Fully Functional API System to manage patient records'}

@app.get('/patients')
def patientsInfo():
    return loadPatientData()


@app.get("/patients/{patient_id}")
def getPatientInfo(patient_id: str =  Path(..., description="ID of the patient", example='P001')):
    patientsData = loadPatientData()
    if patient_id in patientsData:
        return patientsData[patient_id]
    else:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    
    
@app.get("/sortPatientsData")
def SortPatientData(sortBy: str = Query(..., description='Sort on the basis of Height, Weight and BMI'), order: str = Query('asc', description='Sort either in ascending or descending order')):
    
    validFields = ['weight','height','bmi', 'age']
    
    if sortBy not in validFields:
        raise HTTPException(status_code=404, detail='Please Select Among weight, height, bmi and age only')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail='Please select among asc and desc only')
    
    patientsData = loadPatientData()
    
    if order == 'asc':
        return sorted(patientsData.items(), key=lambda x: x[1][sortBy])
    else:
        return sorted(patientsData.items(), key=lambda x: x[1][sortBy], reverse=True)


@app.post('/createPatient')
def createPatient(patient: Patient):
    patientsData = loadPatientData()
    
    if patient.id in patientsData:
        raise HTTPException(status_code=400, detail='Patient Already Exists')
    
    patientsData[patient.id]  = patient.model_dump(exclude=['id'])
    saveData(patientsData)
    
    return JSONResponse(status_code=201, content='Patient Created Successfully')
    
@app.put('/editPatient/{patientID}')
def editPatient(patientID: str, updatedPatientData : PatientUpdate):
    patientsData = loadPatientData()
    
    if patientID not in patientsData:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    
    existingPatientData =  patientsData[patientID]
    
    updatedPatientInfo = updatedPatientData.model_dump(exclude_unset=True)
    
    for key, value in updatedPatientInfo.items():
        existingPatientData[key] = value    
    
    existingPatientData['id'] =  patientID
    
    existingPatientData = Patient(**existingPatientData)
    
    existingPatientData = existingPatientData.model_dump(exclude='id')
    
    patientsData[patientID] = existingPatientData
    
    saveData(patientsData)
    
    return JSONResponse(status_code=200, content='Patient Updated Successfully')

@app.delete('/deletePatient/{patientID}')
def deletePatient(patientID : str):
    
    patientsData = loadPatientData()
    
    if patientID not in patientsData:
        raise HTTPException(status_code=404, detail='Patient doesnt exist')
    
    del patientsData[patientID]
    saveData(patientsData)
    
    return JSONResponse(status_code=200, content='Patient Deleted!')    
     