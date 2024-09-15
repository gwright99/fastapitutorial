from fastapi import APIRouter, FastAPI

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello World!"}


@api_router.get("/healthcheck", status_code=200)
def healthcheck() -> dict:
    """
    Healtcheck GET
    """
    return {"msg": "I aint dead!"}


@api_router.get("/healthcheck/subhealthcheck", status_code=200)
def healthcheck2() -> dict:
    """
    Healtcheck GET
    """
    return {"msg": "I still aint dead!"}


app.include_router(api_router)

if __name__ == "__main__":
    # Use for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="debug")
