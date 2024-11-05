from pathlib import Path
from typing import Any, List, Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from app import crud
from app.db.session import get_db
from app.models.recipe import Recipe as mRecipe
from app.schemas.recipe import Recipe as sRecipe
from app.templates.base import TEMPLATE_FOLDER_PATH_POSIX

router = APIRouter()

# BASE_PATH = Path(__file__).resolve().parents[2]
# TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
TEMPLATES = Jinja2Templates(directory=TEMPLATE_FOLDER_PATH_POSIX)
print(f"Templates string is: {TEMPLATES}")


# Made this `recipes` since `/recipe/view` was caught by `/recipe/{recipe_id}`
@router.get("/recipes/view", status_code=200)
def show_recipes(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
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


from app.schemas.http import HTTP404


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


# @router.post("/recipe", status_code=201, response_model=Recipe)
# def create_recipe(*, recipe_in: RecipeCreate) -> dict:  # 2
#     """
#     Create a new recipe (in memory only)
#     """
#     new_entry_id = len(RECIPES) + 1
#     recipe_entry = Recipe(
#         id=new_entry_id,
#         label=recipe_in.label,
#         source=recipe_in.source,
#         url=recipe_in.url,
#     )
#     RECIPES.append(recipe_entry.dict())  # 3

#     return recipe_entry
