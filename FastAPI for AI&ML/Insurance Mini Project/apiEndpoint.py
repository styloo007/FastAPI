from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.userInput import UserInput
from schema.predictionResponse import PredictionResponse
from model.predict import model, MODEL_VERSION, predictOutput

app = FastAPI()

# Human Readable
@app.get("/")
def home():
    return {'message':'Insurance Premium Category Predictor'}

# Machine Readable (Helps Cloud Services to validate the API Service)
@app.get('/health')
def healthCheck():
    return {
        'status':'OK',
        'version':MODEL_VERSION,
        'model_loaded':model is not None
    }

@app.post('/predict', response_model = PredictionResponse)
def predictPremium(data: UserInput):
    
    inputData = {
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation,
        'city_tier':data.city_tier
    }
    
    prediction = predictOutput(inputData)
    
    return JSONResponse(status_code=200,content={'response':prediction})