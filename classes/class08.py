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

# TODO: Check if the passed language exists!
# TODO: Add the summary option to wikipedia
@app.get("/wiki/search", tags=["Wiki"])
def wiki_search(search_term: str, lang: str = "en"):
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
