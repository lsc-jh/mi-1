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

def get_wiki_result(search_term: str, lang: str):
    langs = wikipedia.languages()
    if lang not in langs:
        return {
            "status": "error",
            "message": "Language not supported.",
            "you_might_want": [l for l in langs if l in lang or lang.startswith(l)]
        }

    wikipedia.set_lang(lang)
    results = wikipedia.search(search_term)
    if len(results) == 0:
        return {
            "status": "error",
            "message": "No results found."
        }

    return {
        "status": "ok",
        "content": results,
    }


@app.get("/wiki/search", tags=["Wiki"])
def wiki_search(search_term: str, lang: str = "en"):
    result = get_wiki_result(search_term, lang)
    if result["status"] == "error":
        return result

    if result["content"][0] == search_term:
        try:
            page = wikipedia.page(search_term)
            return {
                "message": "Page found!",
                "url": page.url,
                "content": page.content
            }
        except wikipedia.exceptions.DisambiguationError as e:
            return {
                "message": "No exact page found, possible options down below",
                "options": e.options
            }

    return {
        "message": "No exact page found, possible links down below",
        "links": [f"https://{lang}.wikipedia.org/wiki/{link}" for link in results]
    }


@app.get("/wiki/summary", tags=["Wiki"])
def wiki_summary(search_term: str, lang: str = "en", sentence: int | None = None):
    result = get_wiki_result(search_term, lang)
    if result["status"] == "error":
        return result

    if result["content"][0] == search_term:
        summary = wikipedia.summary(search_term, sentence)
        return {
            "search_term": search_term,
            "content": summary,
        }









