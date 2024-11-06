import time
from typing import Any

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse

# from app.api.api_v1.router import api_router as v1_router
from app.api.api_v1.router import api_router as v1_router

# from app.apis.base import api_router as master_router
from app.core.config import settings

# from models.models import Add2, Category, Item, items
# from pydantic import BaseModel, EmailStr


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Project to better learn FastAPI and how it aligns with GitOps",
    version="settings.PROJECT_VERSION",
    openapi_url="/openapi.json",
    # docs_url=f"/api/v1/docs",
    # redoc_url=f"/api/v1/redoc",
    root_path="/tutorial",  # <------ Fixes K8s reverse proxy problem.
)


# Define Routers
api_router = APIRouter()
arjan_router = APIRouter()
tiangolo_router = APIRouter()


def include_routers(app):
    # app.include_router(master_router)
    app.include_router(v1_router, prefix=settings.API_V1_STR)


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


# Used to time HTTP response speed.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# @api_router.get("/", status_code=200)
# def root() -> dict[str, str]:
#     """
#     Root GET
#     """
#     return {"msg": "Hello World!"}


# @api_router.get("/healthcheck", status_code=200)
# def healthcheck() -> dict[str, str]:
#     """
#     Healtcheck GET
#     """
#     return {"msg": "I aint dead!"}


# # NOTE: This didn't work initially because HTTPRoute was only allowing GETs through initially.
# # HTTPRoute was modified to not discriminate on HTTP verb. Other verbs like PUT / DELETE should work now too.
# @api_router.post("/add2", status_code=200)
# # def add2(x: int, y: int) -> dict:
# def add2(item: Add2) -> dict[str, int]:
#     # item_dict = item.dict()
#     return {"result": item.x + item.y}


# # Created type to make dictionary definition easier / cleaner.
# Selection = dict[str, str | int | float | Category | None]


# @arjan_router.get("/items", status_code=200)
# def query_item_by_parameters(
#     name: str | None = None,
#     price: float | None = None,
#     count: int | None = None,
#     category: Category | None = None,
# ) -> dict[str, Selection | list[Item]]:
#     # return items
#     def check_item(item: Item) -> bool:
#         # Check all conditions and then return a singular True / False
#         return all(
#             (
#                 name is None or item.name == name,
#                 price is None or item.price == price,
#                 count is None or item.count == count,
#                 category is None or item.category is category,
#             )
#         )

#     # Return any item which matches all selection criteria
#     selection: list[Item] = [item for item in items.values() if check_item(item)]
#     return {
#         "query": {"name": name, "price": price, "count": count, "category": category},
#         "selection": selection,
#     }


# @arjan_router.post("/items", status_code=200)
# def add_item_if_not_exists(item: Item) -> dict[str, Item]:
#     # item.id is mirrored in dict keys
#     if item.id in items.keys():
#         HTTPException(status_code=400, detail=f"Item with {item.id} already exists.")

#     items[item.id] = item
#     return {"added": item}


# @arjan_router.get("/items/{item_id}")
# def query_item_by_id(item_id: int) -> Item:
#     if item_id not in items.keys():
#         raise HTTPException(
#             status_code=404, detail=f"Item with {item_id=} does not exist."
#         )
#     return items[item_id]


# # Updates must come in on query
# @arjan_router.put("/items/{item_id}", status_code=200)
# def update_item(
#     item_id: int = Path(default=..., ge=0),
#     name: str | None = Query(default=None, min_length=1, max_length=8),
#     price: float | None = Query(default=None, gt=0.0),
#     count: int | None = Query(default=None, ge=0),
# ) -> dict[str, Item]:
#     if item_id not in items.keys():
#         HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
#     if all(info for info in (name, price, count)):
#         HTTPException(status_code=404, detail="No parameters provided for update.")

#     print(f"{item_id=}; {count=}; {price=}; {count=}")

#     item = items[item_id]
#     if name is not None:
#         print("Updating name")
#         item.name = name
#     if price is not None:
#         print("Updating price")
#         item.price = price
#     if count is not None:
#         print("Updating count")
#         item.count = count

#     print("Update core list.")
#     items[item_id] = item

#     return {"updated": item}


# # Updates must come in on body since I'm going to use a Pydantic model
# @arjan_router.delete("/items/{item_id}", status_code=200)
# def delete_item(item_id: int, item: Item) -> dict[str, Item]:
#     if item_id not in items.keys():
#         HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")

#     print(f"{item.name=}; {item.count=}")
#     item = items.pop(item_id)
#     return {"deleted": item}


# class Message(BaseModel):
#     message: str
#     message2: str


# from typing import Annotated

# from typing_extensions import TypedDict


# class ResponseDict(BaseModel):
#     id: int
#     payload: dict[str, str]
#     # Call expression not allowed in type expression
#     # stats: TypedDict("Stats", {"age": int, "height": float})
#     stats: Annotated[dict, TypedDict("Stats", {"age": int, "height": float})]
#     name: str = "ipsem lorem"


# class DashboardTest(BaseModel):
#     a: str
#     b: str
#     c: str


# @api_router.get(
#     "/responses/{some_value}",
#     status_code=211,
#     # response_model=ResponseDict,  # dict[str, str],
#     responses={
#         404: {"description": "Item not found."},
#         400: {"description": "Item not available for you, sucker!."},
#         403: {
#             "model": Message
#         },  # These show up as documented responses in the Responses section of each API route on the /docs site.
#         409: {"model": DashboardTest, "description": "Text to show above model."},
#     },
# )
# def tests_responses(
#     some_value: str = Path(
#         default=..., title="Where will this appear in docs?", min_length=1, max_length=8
#     )
# ) -> JSONResponse | ResponseDict:  # dict[str, str]:
#     if some_value == "a":
#         return JSONResponse(status_code=404, content={"message": "aa"})
#     if some_value == "b":
#         return JSONResponse(status_code=400, content={"message": "bb"})
#     if some_value == "c":
#         return JSONResponse(
#             status_code=403, content={"message": "Blah", "message2": "Balh2"}
#         )

#     # return {"id": 1, "payload": {"a": "a"}}  # , "stats": {"age": 42, "height": 6.2}}
#     return ResponseDict(id=1, payload={"a": "a"}, stats={"age": 42, "height": 6.2})
#     # return dict(a=1, fred=2)


# # https://fastapi.tiangolo.com/tutorial/response-model/#return-the-same-input-data
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# # This takes 4 values in, but only returns 3 (based on )
# @tiangolo_router.post("/user", response_model=UserOut)
# def create_user(user: UserIn) -> Any:
#     return user


app.include_router(router=api_router)
app.include_router(router=arjan_router)
app.include_router(router=tiangolo_router)

include_routers(app)


# Putting these into a if __name__ == '__main__' block seems not to execute since program
# is run via `fastapi run scr/app/app.py --port xxxx --reload`


# I don't understand why this pulls in 3 children models.
# HOWEVER, this seem the import statement seems essential or else you get the following error when
# trying to add a user:
#    sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[User(user)],
#    expression 'Blog' failed to locate a name ('Blog'). If this is a class name, consider
#    adding this relationship() to the <class 'db.models.user.User'> class after both dependent
#    classes have been defined.
# from db.base import Base

# def create_tables():
#     Base.metadata.create_all(bind=engine)
# create_tables()

# https://stackoverflow.com/questions/74116435/fastapi-is-not-quitting-when-pressing-ctrc
# def receive_signal(signalNumber, frame):
#     print("Received:", signalNumber)
#     sys.exit()


# @app.on_event("startup")
# async def startup_event():
#     import signal

#     signal.signal(signal.SIGINT, receive_signal)

# Must be like this or we break testing due to import of app.main
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="debug")
