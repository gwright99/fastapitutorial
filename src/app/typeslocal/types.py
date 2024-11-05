from datetime import datetime
from typing import List, MutableMapping, Optional, TypeAlias, Union

# from app.models.blog import Blog

# UpdateBlogResponse: TypeAlias = dict[str, str] | Blog

JWTPayloadMapping: TypeAlias = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]
