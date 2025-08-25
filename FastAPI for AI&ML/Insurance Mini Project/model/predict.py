import pickle
import pandas as pd

with open("model/model.pkl", "rb") as f:
    model =  pickle.load(f)
    
MODEL_VERSION = "1.0.0"

def predictOutput(userInput: dict):
    inputDF =  pd.DataFrame(userInput, index=[0])
    output = model.predict(inputDF)
    return output[0]