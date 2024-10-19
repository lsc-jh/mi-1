# FastAPI example
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    return {"status": "up"}

@app.get("/calculate")
def calculate():
    """This function adds two numbers togehter."""
    a = 3
    b = 5
    result = a + b

    return {
        "a": a,
        "b": b,
        "result": result
    }
