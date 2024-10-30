from db.models.blog import Blog
from schemas.blog import CreateBlog, UpdateBlog
from sqlalchemy import update
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: int = 1):
    # blog: Blog = Blog(**blog.dict(), author_id=author_id)
    blog: Blog = Blog(**blog.model_dump(), author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def list_blogs(db: Session):
    # Changed `==` to `.is_` to avoid flake8 error
    # https://stackoverflow.com/questions/18998010/flake8-complains-on-boolean-comparison-in-filter-clause
    blogs = db.query(Blog).filter(Blog.is_active.is_(True)).all()
    return blogs


def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
    # Original code. Threw Pylance error:
    # blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    # if not blog_in_db:
    #     return
    # blog_in_db.title = blog.title
    # blog_in_db.content = blog.content
    # db.add(blog_in_db)
    # db.commit()
    # return blog_in_db

    # THIS WORKS
    # Warning - using first get a SQLAlchemy Blog Model rather than the query itself.
    blog_in_db = db.query(Blog).filter(Blog.id == id)  # .first()
    blog_in_db.update(values={"title": blog.title, "content": "ipsem2"})
    # db.add(blog_in_db)
    db.commit()

    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    # db.refresh(blog_in_db)  # This line fails
    return blog_in_db


def delete_blog(id: int, author_id: int, db: Session):
    """
    Notice the use of .first(): `blog_in_db = db.query(Blog).filter(Blog.id == id).first()` returns an actual Blog object.
    This blog object has no `delete()` method defined, instead work with Query object.
    """

    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    blog_in_db.delete()
    db.commit()
    return {"msg": f"deleted blog with id {id}"}


# Note different use of .first() between these 2 protected endpoints.
# Is this on purpose or because author is just inconsistent?
def protected_update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:  # new
        return {"error": f"Only the author can modify the blog"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def protected_delete_blog(id: int, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    if not blog_in_db.first().author_id == author_id:  # new
        return {"error": f"Only the author can delete a blog"}
    blog_in_db.delete()
    db.commit()
    return {"msg": f"deleted blog with id {id}"}
