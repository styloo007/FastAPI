from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="A Simple Calculator Application",
    description="A Simple Calculator Application doing basic operations between two numbers",
    version="1.0.0"
    
)

# Pydantic Model for requesting bodies

class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResult(BaseModel):
    operation: str
    a: float
    b: float
    result: float
    
@app.get("/")
def welcome():
    return {"message":"Welcome to the Calculator App", "docs":"/docs"}

@app.get("/add/{a}/{b}")
def addition(a:float,b:float):
    return CalculationResult(
        operation = "addition",
        a = a,
        b = b,
        result=a + b 
    )


@app.get("/subtract/{a}/{b}")
def subtract(a:float, b:float):
    return CalculationResult(
        operation="Subtraction",
        a = a,
        b = b,
        result= a-b
    )
    
@app.get("/multiply/{a}/{b}")
def product(a:float, b:float):
    return CalculationResult(
        operation = "Multiplication",
        a = a,
        b = b,
        result=a*b
    )
    
    
@app.get("/divide/{a}/{b}")
def divide(a:float, b:float):
    return CalculationResult(
        operation = "Division",
        a = a,
        b = b,
        result=a/b
    )
    
@app.post("/mutliplyAdvanced")
def multiplyAdvanced(calc: CalculationRequest):
    return CalculationResult(
        operation= "Advanced Method for Multiplication",
        a =  calc.a,
        b = calc.b,
        result= calc.a * calc.b
    )
    
@app.post("/divisionAdvanced")
def divisionAdvanced(calc: CalculationRequest):
    
    if calc.b == 0:
        raise HTTPException(status_code=400, detail = "Cannot divide by zero")
    
    return CalculationResult(
        operation="Advance Method for Division",
        a =  calc.a,
        b =  calc.b,
        result = calc.a / calc.b
    )

@app.post("/power")
def power(calc: CalculationRequest):
    return CalculationResult(
        operation= "Power",
        a = calc.a,
        b = calc.b,
        result= calc.a ** calc.b
    )

@app.get("/calculate")
def calculate(operation:str, a:float, b:float):
    operations = {
        "add":a+b,
        "sub":a-b,
        "mul":a*b,
        "div":a/b,
        "power":a**b
    }    
    
    if operation not in operations:
        raise HTTPException(status_code=400, detail=f"Invalid Operation. Choose from: {list(operations.keys())}" )
    
    if operation=="divide" and b==0:
        raise HTTPException(status_code=400, detail="Cannot Divide a number by 0")
    
    return CalculationResult(
        operation=operation,
        a=a,
        b=b,
        result=operations[operation]
    )