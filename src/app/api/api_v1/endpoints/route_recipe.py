import asyncio
from pathlib import Path
from typing import Any, List, Optional, Sequence

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from app import crud
from app.clients.reddit import RedditClient
from app.core.auth import oauth2_scheme
from app.dependencies.dependencies import (
    caller_has_superuser_status,
    get_current_user,
    get_db,
    get_reddit_client,
)
from app.models.recipe import Recipe as mRecipe
from app.models.user import User
from app.schemas.http import HTTP404
from app.schemas.recipe import Recipe as sRecipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeUpdateRestricted
from app.templates.base import TEMPLATE_FOLDER_PATH_POSIX

router = APIRouter()
RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]

# BASE_PATH = Path(__file__).resolve().parents[2]
# TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
TEMPLATES = Jinja2Templates(directory=TEMPLATE_FOLDER_PATH_POSIX)
print(f"Templates string is: {TEMPLATES}")


# Made this `recipes` since `/recipe/view` was caught by `/recipe/{recipe_id}`
@router.get("/recipe/all", status_code=200)
def view_all_recipes(
    request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> HTMLResponse:
    """

    Args:
        request (Request): The request sent to FastAPI.
        db (Session, optional): App DB. Defaults to Depends(get_db).

    Returns:
        HTMLResponse: Jinja2 Templated answer.
    """
    print(f"Templates string is: {TEMPLATES}")
    recipes: List[mRecipe] = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": recipes},
    )


@router.get(
    "/recipe/{recipe_id}",
    status_code=200,
    response_model=sRecipe,
    responses={
        404: {"model": HTTP404, "description": "Recipe ID Not Found In Database."}
    },
)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Fetch a single recipe by ID
    """

    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        # Returning Exception will cause Pydantic validation error. Raise Exception instead.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found."
        )

    return result


# # Query enforces additional rules on the sort of string payload that can be sent. E.g
# # curl -X 'GET' 'http://localhost:8081/tutorial/recipes/search?keyword=ab&max_results=10' \
# #   -H 'accept: application/json'
# @router.get("/recipes/search", status_code=200, response_model=RecipeSearchResults)
# def search_recipes(
#     *,
#     keyword: Optional[str] = Query(None, min_length=3, example="chicken"),  # 2
#     max_results: Optional[int] = 10,
# ) -> dict:
#     """
#     Search for recipes based on label keyword
#     """
#     if not keyword:
#         # we use Python list slicing to limit results
#         # based on the max_results query parameter
#         return {"results": RECIPES[:max_results]}

#     results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)

#     payload = {"results": list(results)[:max_results]}
#     print(len(payload["results"]))
#     return payload


@router.post("/", status_code=201, response_model=RecipeCreate)
def create_recipe(
    *,
    recipe_in: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> mRecipe:
    """
    Create a new recipe in the database.
    """
    if recipe_in.submitter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit recipes as yourself"
        )
    recipe: mRecipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe


@router.put("/", status_code=201, response_model=RecipeUpdate)
def update_recipe(
    *,
    recipe_in: RecipeUpdateRestricted,
    db: Session = Depends(get_db),
) -> mRecipe:
    """
    Update recipe in the database.
    """
    recipe = crud.recipe.get(db, id=recipe_in.id)
    if not recipe:
        raise HTTPException(
            status_code=400, detail=f"Recipe with ID: {recipe_in.id} not found."
        )

    # if recipe.submitter_id != current_user.id:
    #     raise HTTPException(
    #         status_code=403, detail=f"You can only update your recipes."
    #     )

    updated_recipe = crud.recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)
    db.commit()
    return updated_recipe


async def get_reddit_top_async(subreddit: str) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "recipe bot 0.1"},
        )

    subreddit_recipes = response.json()
    subreddit_data = []
    for entry in subreddit_recipes["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    return subreddit_data


# This endpoint needs the user to be a superuser in order to call it.
@router.get("/ideas/async", description="Will reject anyone not a superuser.")
async def fetch_ideas_async(
    user: User = Depends(caller_has_superuser_status),
) -> dict:
    results = await asyncio.gather(
        *[get_reddit_top_async(subreddit=subreddit) for subreddit in RECIPE_SUBREDDITS]
    )
    return dict(zip(RECIPE_SUBREDDITS, results))


# This clashed with `/{recipe_id}` had to add namespace above for API route separation.
@router.get("/ideas")
def fetch_ideas(reddit_client: RedditClient = Depends(get_reddit_client)) -> dict:
    return {
        key: reddit_client.get_reddit_top(subreddit=key) for key in RECIPE_SUBREDDITS
    }
