from typing import List

from apis.v1.route_login import get_current_user
from db.models.blog import Blog
from db.models.user import User
from db.repository.blog import (
    create_new_blog,
    delete_blog,
    list_blogs,
    protected_delete_blog,
    protected_update_blog,
    retrieve_blog,
    update_blog,
)
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
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


@router.get("/blogs", response_model=List[ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    return blogs


@router.put("/blog/{id}", response_model=ShowBlog)
def update_a_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    blog = update_blog(id=id, blog=blog, author_id=1, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with id {id} does not exist")
    return blog


@router.delete("/delete/{id}")
def delete_a_blog(id: int, db: Session = Depends(get_db)):
    message = delete_blog(id=id, author_id=1, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": f"Successfully deleted blog with id {id}"}


# Protected Versions of same APIs Above
from app.typeslocal.types import UpdateBlogResponse


@router.put("/blog/protected/{id}", response_model=ShowBlog)
def protected_update_a_blog(
    id: int,
    blog: UpdateBlog,
    db: Session = Depends(dependency=get_db),
    current_user: User = Depends(dependency=get_current_user),
):
    # new_blog: dict[str, str] | Blog = protected_update_blog(
    new_blog: UpdateBlogResponse = protected_update_blog(
        id=id, blog=blog, author_id=current_user.id, db=db
    )
    if isinstance(blog, dict):
        raise HTTPException(
            detail=blog.get("error"),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return new_blog


@router.delete("/blog/protected/{id}")
def protected_delete_a_blog(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = protected_delete_blog(id=id, author_id=current_user.id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"msg": f"Successfully deleted blog with id {id}"}
