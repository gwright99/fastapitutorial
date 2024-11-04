import logging

from sqlalchemy.orm.session import Session

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Creating initial data")
    db: Session = SessionLocal()
    init_db(db)
    logger.info("Initial data created")
