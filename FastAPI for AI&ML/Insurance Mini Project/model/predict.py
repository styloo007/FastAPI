import pickle
import pandas as pd

with open("model/model.pkl", "rb") as f:
    model =  pickle.load(f)
    
MODEL_VERSION = "1.0.0"

classLabels = model.classes_.tolist()

def predictOutput(userInput: dict):
    inputDF =  pd.DataFrame([userInput])
    predictedClass = model.predict(inputDF)
    probabilities = model.predict_proba(inputDF)[0]
    confidence = max(probabilities)
    classProbs = dict(zip(classLabels, map(lambda p:round(p,4),probabilities)))
    
    return {
        'predicted_category':predictedClass[0],
        'confidence':round(confidence,4),
        'class_probabilities':classProbs
    }