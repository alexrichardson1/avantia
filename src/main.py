from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .db import seed, get_collection
from fuzzywuzzy import fuzz


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed()
    app.collection = get_collection()
    yield


app = FastAPI(lifespan=lifespan)


def _fuzzy_search(query: str, field: str):
    THRESHOLD = 80
    collection = get_collection()

    all_entries = collection.find({}, {field: 1, "_id": 0})
    results = []

    for entry in all_entries:
        field_value = entry.get(field, "")
        score = fuzz.ratio(query.lower(), field_value.lower())
        if score >= THRESHOLD:
            results.append({field: field_value, "score": score})

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return [x[field] for x in sorted_results]


def _raise_if_empty(results) -> None:
    if not results:
        raise HTTPException(status_code=404, detail="No laureates found")


@app.get("/search/name/")
async def search_by_name(name: str):
    first_name_results = _fuzzy_search(name, "firstname")
    surname_results = _fuzzy_search(name, "surname")

    results = first_name_results + surname_results
    _raise_if_empty(results)
    return [document for document in results]


@app.get("/search/category/")
async def search_by_category(category: str):
    results = _fuzzy_search(category, "category")
    _raise_if_empty(results)
    return [document for document in results]


@app.get("/search/motivation/")
async def search_by_motivation(motivation: str):
    results = _fuzzy_search(motivation, "motivation")
    _raise_if_empty(results)
    return [document for document in results]
