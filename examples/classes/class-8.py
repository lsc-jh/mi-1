from fastapi import FastAPI
import timeit
from pydantic import BaseModel
import wikipedia

class BaseOperation(BaseModel):
    text: str


start = timeit.default_timer()

tags_metadata = [
    {
        "name": "Home",
        "description": "Base endpoints."
    },
    {
        "name": "Wiki",
        "description": "Endpoints for porting wikipedia."
    },
    {
        "name": "AI",
        "description": "Everything that AI."
    }
]


app = FastAPI(
    openapi_tags=tags_metadata,
)

@app.get("/", tags=["Home"])
def root():
    current_time = timeit.default_timer()
    return {
        "status": "up",
        "uptime": current_time - start
    }

class WikiResponse:
    def __init__(self, message: str, status: str, content):
        self.message = message
        self.status = status
        self.content = content

    def has_page(self):
        return self.content is not None

    def __str__(self):
        return f"WikiResponse: {self.message}"

def get_wiki_page(search_term: str, lang: str = "en"):
    langs = wikipedia.languages()
    if lang not in langs:
        return WikiResponse("Invalid language", "error", None)
    try:
        return wikipedia.page(search_term)
    except wikipedia.exceptions.DisambiguationError as e:
        return WikiResponse("Disambiguation error", "error", e.options)
    except wikipedia.exceptions.PageError:
        return WikiResponse("Page not found", "error", None)

@app.get("/wiki/search", tags=["Wiki"])
def wiki_search(search_term: str, lang: str = "en"):
    langs = wikipedia.languages()
    if lang not in langs:
        return {
            "status": "error",
            "message": "Invalid language"
        }

    wikipedia.set_lang(lang)
    results = wikipedia.search(search_term)
    if len(results) == 0:
        return {"message": "No results found."}

    if results[0] == search_term:
        page = wikipedia.page(search_term)
        return {
            "message": "Page found!",
            "url": page.url,
            "content": page.content
        }

    return {
        "message": "No exact page found, possible links down below",
        "links": [f"https://{lang}.wikipedia.org/wiki/{link}" for link in results]
    }

@app.get("/wiki/summary{search_term}", tags=["Wiki"])
def wiki_summary(search_term: str, lang: str = "en"):
    langs = wikipedia.languages()
    if lang not in langs:
        return {
            "status": "error",
            "message": "Invalid language"
        }

    wikipedia.set_lang(lang)
    try:
        page = wikipedia.page(search_term)
        return {
            "message": "Page found!",
            "url": page.url,
            "content": page.content
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {
            "message": "Disambiguation error",
            "options": e.options
        }
    except wikipedia.exceptions.PageError:
        return {
            "message": "Page not found"
        }