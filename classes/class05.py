# FastAPI example
import re
from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def welcome():
    return {"status": "up"}

@app.get("/calculate")
def calculate(a: int, b: int):
    """This function adds two numbers togehter."""
    result = a + b

    return {
        "a": a,
        "b": b,
        "result": result
    }

@app.get("/calculate/{a}/{b}")
def calculate_with_path(a: int, b: int, operator: Literal["+", "-", "*", "/"] = "+"):
    """ABC"""

    match operator:
        case "+":
            result = a + b
        case "-":
            result = a - b
        case "*":
            result = a * b
        case "/":
            result = a / b

    return {
        "a": a,
        "b": b,
        "operator": operator,
        "result": result if result else "Some of the inputs were incorrect!"
    }

class Request(BaseModel):
    a: int
    b: int
    operation: str = "+"

class Operation(BaseModel):
    message: str

@app.post("/calculate")
def calculate_post(req: Request):
    a, b, operator = req.a, req.b, req.operation

    match operator:
        case "+":
            result = a + b
        case "-":
            result = a - b
        case "*":
            result = a * b
        case "/":
            result = a / b
        case _:
            result = None

    return {
        "a": a,
        "b": b,
        "operator": operator,
        "result": result if result != None else "Some of the inputs were incorrect!"
    }





