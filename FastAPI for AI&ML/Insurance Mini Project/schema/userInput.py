from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Annotated, Optional, Literal
from config.cityTier import tier1Cities,tier2Cities

class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0,lt=120, description="Age of the User")]
    weight: Annotated[float, Field(...,gt=0,lt=200, description="Weight of the User in KGs")]
    height: Annotated[float, Field(...,gt=0,lt=2.5, description="Height of the User in Metres")]
    income_lpa: Annotated[float, Field(...,gt=0, description="Annual Salary of the User in Lakhs")]
    smoker: Annotated[bool, Field(...,description="Does the User Smoke?")]
    city: Annotated[str, Field(...,description="City of the User")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...,description="Occupation of the User")]
    
    @field_validator('city')
    @classmethod
    def normalizeCity(cls,v:str)->str:
        v = v.strip().title()
        return v
    
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
        
