from pathlib import Path
from typing import Any, Optional, Sequence

from fastapi import APIRouter, FastAPI, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl

router = APIRouter()

BASE_PATH = Path(__file__).resolve().parents[2]
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
print(f"Templates string is: {TEMPLATES}")

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]


class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl


class RecipeSearchResults(BaseModel):
    #  Sequence (which is an iterable with support for len and __getitem__)
    results: Sequence[Recipe]


class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


@router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> Any:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        # 2
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result[0]


# Query enforces additional rules on the sort of string payload that can be sent. E.g
# curl -X 'GET' 'http://localhost:8081/tutorial/recipes/search?keyword=ab&max_results=10' \
#   -H 'accept: application/json'
@router.get("/recipes/search", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),  # 2
    max_results: Optional[int] = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)

    payload = {"results": list(results)[:max_results]}
    print(len(payload["results"]))
    return payload


@router.post("/recipe", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:  # 2
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())  # 3

    return recipe_entry


# Had o make this recipes since `/recipe/view` had view being interpreted as value to pass
# to other .get at (`/recipe/{recipe_id}`)
@router.get("/recipes/view", status_code=200)
def show_view(request: Request) -> dict:
    print(f"Templates string is: {TEMPLATES}")
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES},
    )
