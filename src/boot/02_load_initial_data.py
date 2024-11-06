import logging

from sqlalchemy.orm.session import Session

# Packages autoload related classes via __init__.py
from app import crud, models, schemas  # noqa: F401
from app.assets.recipe_data import RECIPES
from app.core.config import settings
from app.dependencies.dependencies import get_db
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def init_db(db: Session) -> None:
    # Create superusers if they are defined in `app/core/config`
    for superuser in settings.SUPERUSERS:
        user = crud.user.get_by_email(db, email=superuser.email)
        if not user:
            logger.debug("=== CREATING USER")
            # Change Schema `UserBase` to `UserCreate``
            user_in: UserCreate = UserCreate.model_validate(superuser.model_dump())
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.debug(f"Superuser {superuser.email} already exists.")

        # If superuser newly-created, recipes will be empty. If already-existing, ensure recipes present.
        if not user.recipes:
            for index, recipe in enumerate(RECIPES):
                # Assign odd recipes to one admin and evens to the other
                recipe_in = schemas.RecipeCreate(**recipe, submitter_id=(index % 2) + 1)

                crud.recipe.create(db, obj_in=recipe_in)


if __name__ == "__main__":
    logger.info("Creating initial data")

    db: Session = next(get_db())
    init_db(db=db)

    logger.info("Initial data created")
