import logging
import os

from sqlalchemy.orm.session import Session

print("CWD")
print(os.getcwd())
# Packages autoload related classes via __init__.py
from app import crud, models, schemas  # noqa: F401
from app.assets.recipe_data import RECIPES
from app.core.config import settings
from app.db.session import SessionLocal

# Traceback (most recent call last):
#   File "/home/deeplearning/fastapitutorial/src/app/boot_02_load_initial_data.py", line 6, in <module>
#     from app import crud, models, schemas  # noqa: F401
#   File "/home/deeplearning/fastapitutorial/src/app/app.py", line 9, in <module>
#     from app.api.api_v1.router import api_router as v1_router
# ModuleNotFoundError: No module named 'app.api'; 'app' is not a package


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# FIRST_SUPERUSER = "admin@recipeapi.com"


def init_db(db: Session) -> None:
    # if FIRST_SUPERUSER:
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            print("=== CREATING USER")
            user_in = schemas.user.UserCreate(
                full_name="Robert Superuser",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
                password="abcdef",
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                f"Skipping superuser creation. Email {settings.FIRST_SUPERUSER} already exists. "
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


if __name__ == "__main__":
    logger.info("Creating initial data")

    db: Session = SessionLocal()
    init_db(db)

    logger.info("Initial data created")
