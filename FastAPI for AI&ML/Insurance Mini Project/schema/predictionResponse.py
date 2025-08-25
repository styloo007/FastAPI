from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

class PredictionResponse(BaseModel):
    predicted_category : Literal['High','Medium','Low'] = Field(...,description="Predicted Insurance Premium Category ", example="High")
    confidence : float = Field(..., description="Confidence of the Predicted Class", example="0.66")
    class_probabilities : Dict[str,float] = Field(..., description="Probabilities distribution across all the classes", example={'Low':0.2,'Medium':0.66,'High':0.2})