from typing import TypeAlias

from db.models.blog import Blog

UpdateBlogResponse: TypeAlias = dict[str, str] | Blog
