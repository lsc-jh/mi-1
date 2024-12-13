import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import webbrowser
import _thread
from time import sleep
from jsonservice import JsonService

def abs_path(rel_path):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dir_name, rel_path))


def open_browser():
    sleep(2)
    if os.path.exists("game.html"):
        webbrowser.open_new("game.html")


description = """An Adventure game where you can explore a new world!

By: [joshika39](https://github.com/joshika39)
"""

SERVER_URL="http://localhost:8000"

service = JsonService('users.json')

user_states = service.read("users") if service.read("users") else {}

with open('scenes.json') as f:
    scenes = json.load(f)
app = FastAPI(
    description=description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Adventure"])
def home():
    return {
        "message": "Hello Adventurer!",
        "possible_routes": [
            f"GET;{SERVER_URL}/start;Start Game",
            f"POST;{SERVER_URL}/continue;Continue Game",
            f"GET;{SERVER_URL}/save;Save Game",
            f"GET;{SERVER_URL}/load;Load Game"
        ]
    }


@app.get("/start", tags=["Adventure"])
def start(user: str):
    if user is None or user == "" or user == "null":
        raise HTTPException(status_code=400, detail="Please enter a valid user name.")
    _users = service.read("users")

    if user not in user_states and user not in _users:
        user_states[user] = "start"
        service.write(f'users.{user}', "start")
        return {
            "message": f"Welcome {user}!",
            "scene": scenes["start"]
        }
    return {
        "message": f"Welcome back {user}!",
        "scene": scenes[user_states[user]]
    }

@app.get("/save", tags=["Adventure"])
def save(user: str):
    if user not in user_states:
        raise HTTPException(status_code=404, detail=f"Game not started for {user}")

    service.write(f'users.{user}', user_states[user])
    return {
        "message": f"Game saved for {user}",
        "scene": user_states[user]
    }

class GameChoice(BaseModel):
    user: str
    choice: str

@app.post('/continue', tags=["Adventure"])
def continue_game(body: GameChoice):
    user = body.user
    choice = body.choice

    if user not in user_states:
        raise HTTPException(status_code=404, detail=f"Game not started for {user}")

    current_scene = user_states[user]
    if choice not in scenes[current_scene]["choices"]:
        raise HTTPException(status_code=404, detail=f"Not a valid choice for {choice}")

    user_states[user] = choice
    next_scene = scenes[choice]
    return {
        "message": "Success",
        "scene": next_scene
    }


if __name__ == "__main__":
    _thread.start_new_thread(open_browser, ())
    uvicorn.run("main:app", reload=True)
