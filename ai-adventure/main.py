from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import webbrowser
import _thread
from time import sleep
from jsonservice import JsonService
import requests
import json
from pydantic import BaseModel

SERVER_URL = "http://localhost:8000"
AI_URL = "https://lsc-ai.kou-gen.net/api/generate"
PROMPT_URL = "https://lsc-ai.kou-gen.net/prompt/mi-1/v1/generate"

service = JsonService('users.json')

class User:
    def __init__(self, username: str, json_data=None):
        self.username = username

        if json_data:
            self.current_scene = json_data["current_scene"]
            self.scene = json_data["scene"]
            self.scene_count = json_data["scene_count"]
            self.max_scenes = json_data["max_scenes"]
        else:
            self.current_scene = "start"
            self.scene_count = 0
            self.max_scenes = 10
            self.scene = {}

    def generate_next_scene(self, choice=None, model="llama3"):
        if self.scene_count >= self.max_scenes:
            return

        self.scene_count += 1

        choices = list(self.scene.get("choices", {}).values())

        body = {
            "scene": self.current_scene,
            "choices": choices,
            "context": self.scene.get("description", ""),
            "choice": choice,
            "scene_count": self.scene_count,
            "max_scenes": self.max_scenes
        }

        prompt_res = requests.post(PROMPT_URL, json=body)

        if prompt_res.status_code == 200:
            raw_json = prompt_res.json()
            prompt = raw_json.get("prompt")
        else:
            print("Error:", prompt_res.text)
            return None

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(AI_URL, json=payload)

        try:
            if response.status_code == 200:
                self.scene = json.loads(response.json().get("response"))
                self.current_scene = self.scene["name"]

                service.write(f"users.{self.username}", self.serialize())
            else:
                print("Error:", response.text)
                return None
        except:
            print("Error:", response.text)
            return None


    def serialize(self):
        return {
            "current_scene": self.current_scene,
            "scene": self.scene,
            "scene_count": self.scene_count,
            "max_scenes": self.max_scenes
        }


def open_browser(*args) -> None:
    sleep(2)
    if os.path.exists("game.html"):
        webbrowser.open_new("game.html")


app = FastAPI()

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
    }


@app.get("/start")
def start_game(username: str, max_scenes: int = 10, language: str = "en"):
    user = service.read(f"users.{username}")

    if not user:
        user = User(username)
        user.max_scenes = max_scenes # Uj sor
        service.write(f"users.{username}", user.serialize())
        user.generate_next_scene()
    else:
        user = User(username, user)

    return user.serialize()

class GameChoice(BaseModel):
    username: str
    choice: str

@app.post("/continue")
def continue_game(game_choice: GameChoice):
    username = game_choice.username
    choice = game_choice.choice

    user = service.read(f"users.{username}")

    if not user:
        return {
            "message": "User not found!"
        }

    user = User(username, user)

    if not user.scene:
        return {
            "message": "Scene not found! Go to /start!"
        }

    if choice not in user.scene["choices"]:
        return {
            "message": "Invalid choice!"
        }

    user.generate_next_scene(choice)

    return user.serialize()



if __name__ == "__main__":
    #_thread.start_new_thread(open_browser, ())
    uvicorn.run("main:app", reload=True)
