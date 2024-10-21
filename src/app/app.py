from fastapi import APIRouter, FastAPI, HTTPException, Request

# from pydantic import BaseModel
from models.models import Add2, Category, Item, items

app = FastAPI(
    title="Recipe API",
    openapi_url="/openapi.json",
    # docs_url=f"/api/v1/docs",
    # redoc_url=f"/api/v1/redoc",
    root_path="/tutorial",  # <------ Fixes K8s reverse proxy problem.
)

api_router = APIRouter()

arjan_router = APIRouter()


# Problem with handling trailing slash in browser
# K8s HTTPRoute can rewrite prefixes but circa Sept 2024 seems unable to change suffixed easily.
# Routing implementing in 2 parts:
#  1) Use of common `fastapi.grahamwrightk8s.net` DOMAIN means first part of prefix
#     must identify target app (which HTTPRoute filter rewrites).
#  2) FastAPI middleware processes request path prior to sending to FastAPI router
#     and removes trailing slash for anything other than `/`.

# Background:
# https://peakd.com/hive-110369/@brianoflondon/forward-slash-hell-how-one-character-cost-me-a-day
# https://github.com/fastapi/fastapi/discussions/9328


# Solution:
# https://stackoverflow.com/questions/75726959/how-to-reroute-requests-to-a-different-url-endpoint-in-fastapi
# https://stackoverflow.com/questions/74009210/how-to-create-a-fastapi-endpoint-that-can-accept-either-form-or-json-body/74015930#74015930
# BG issue has some extra flags for FastAPI which might work but explicit method seems cleaner to me.
@app.middleware("http")
async def some_middleware(request: Request, call_next):

    # See PKB for why the null check needs to happen (TestClient vs K8s HTTPRoute rewrite)
    print("request.url.path:", request.url.path)
    if ((request.url.path)[-1] == "/") and ((request.scope["path"])[0:-1] != ""):
        request.scope["path"] = (request.scope["path"])[0:-1]

    return await call_next(request)


@api_router.get("/", status_code=200)
def root() -> dict[str, str]:
    """
    Root GET
    """
    return {"msg": "Hello World!"}


@api_router.get("/healthcheck", status_code=200)
def healthcheck() -> dict[str, str]:
    """
    Healtcheck GET
    """
    return {"msg": "I aint dead!"}


@api_router.get("/healthcheck/subhealthcheck", status_code=200)
def healthcheck2() -> dict[str, str]:
    """
    Healtcheck GET
    """
    return {"msg": "I still aint dead!"}


# NOTE: This didn't work initially because HTTPRoute was only allowing GETs through initially.
# HTTPRoute was modified to not discriminate on HTTP verb. Other verbs like PUT / DELETE should work now too.
@api_router.post("/add2", status_code=200)
# def add2(x: int, y: int) -> dict:
def add2(item: Add2) -> dict[str, int]:
    # item_dict = item.dict()
    return {"result": item.x + item.y}


# Created type to make dictionary definition easier / cleaner.
Selection = dict[str, str | int | float | Category | None]


@arjan_router.get("/items", status_code=200)
def query_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    # return items
    def check_item(item: Item) -> bool:
        # Check all conditions and then return a singular True / False
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            )
        )

    # Return any item which matches all selection criteria
    selection: list[Item] = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@arjan_router.post("/items", status_code=200)
def add_item_if_not_exists(item: Item) -> dict[str, Item]:
    # item.id is mirrored in dict keys
    if item.id in items.keys():
        HTTPException(status_code=400, detail=f"Item with {item.id} already exists.")

    items[item.id] = item
    return {"added": item}


@arjan_router.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items.keys():
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )
    return items[item_id]


app.include_router(router=api_router)
app.include_router(router=arjan_router)

if __name__ == "__main__":
    # Use for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="debug")
