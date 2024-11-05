import logging

from sqlalchemy.orm.session import Session

# Packages autoload related classes via __init__.py
from app import crud, models, schemas  # noqa: F401
from app.assets.recipe_data import RECIPES
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

FIRST_SUPERUSER = "admin@recipeapi.com"


def init_db(db: Session) -> None:
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            print("=== CREATING USER")
            user_in = schemas.user.UserCreate(
                full_name="Robert Superuser",
                email=FIRST_SUPERUSER,
                is_superuser=True,
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


if __name__ == "__main__":

    logger.info("Creating initial data")

    db: Session = SessionLocal()
    init_db(db)

    logger.info("Initial data created")
