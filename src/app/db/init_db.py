import logging

from app import (  # Relies on __init__.py to pull in classes in the package.
    crud,
    schemas,
)
from app.assets.recipe_data import RECIPES
from app.db import base  # noqa: F401
from app.db.session import Session

# from app.models import Blog

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@recipeapi.com"


def init_db(db: Session) -> None:
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            print("========================================== CReATING USER")
            user_in = schemas.user.UserCreate(
                # full_name="Initial Super User",
                email=FIRST_SUPERUSER,
                # is_superuser=True,
                password="abcdef",
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                f"Skipping superuser creation. Email {FIRST_SUPERUSER} already exists. "
            )

        # TODO: Figure out how this relationship is being used.
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=recipe["label"],
                    source=recipe["source"],
                    url=recipe["url"],
                    submitter_id=user.id,
                )
                crud.recipe.create(db, obj_in=recipe_in)
