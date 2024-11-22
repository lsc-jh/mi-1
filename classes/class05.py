from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chatbot import Chat, register_call
import wikipedia

from transformers import file_utils
print(file_utils.default_cache_path)

exit()

# Just example :-)
tags_metadata = [
    {
        "name": "calculate",
        "description": "Operations to calculate numbers."
    }
]

app = FastAPI(
    openapi_tags=tags_metadata
)


@app.get("/")
def welcome():
    return {"status": "up"}

@app.get("/calculate", tags=["calculate"])
def calculate(a: int, b: int):
    """This function adds two numbers togehter."""
    result = a + b

    return {
        "a": a,
        "b": b,
        "result": result
    }

@app.get("/calculate/{a}/{b}", tags=["calculate"])
def calculate_with_path(a: int, b: int, operator: Literal["+", "-", "*", "/"] = "+"):
    """ABC"""

    print(f"Operator: {operator}")
    print(f"a: {a}")
    print(f"b: {b}")

    result = None

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

@app.post("/calculate", tags=["calculate"])
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
        "result": result if result is not None else "Some of the inputs were incorrect!"
    }


class Operation(BaseModel):
    message: str

@app.post("/ai/chat")
def ai_chat(op: Operation):
    text = op.message
    if text is None or text == "":
        raise HTTPException(status_code=418, detail="Message is empty!")
    chat = Chat()
    return chat.respond(text)


