from db.repository.blog import create_new_blog, retrieve_blog
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/blog/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog
