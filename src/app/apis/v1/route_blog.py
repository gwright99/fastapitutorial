from db.repository.blog import create_new_blog
from db.session import get_db
from fastapi import APIRouter, Depends, status
from schemas.blog import CreateBlog, ShowBlog
from sqlalchemy.orm import Session

router = APIRouter()


# TODO: Align these names with underlying repository call
@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(
        blog=blog, db=db, author_id=1
    )  # TODO: Make author_id variable.
    return blog
