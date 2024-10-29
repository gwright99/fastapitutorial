from datetime import datetime
from datetime import timezone

from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship


class Blog(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    # Capture timestamps in UTC: https://stackoverflow.com/questions/2331592/why-does-datetime-datetime-utcnow-not-contain-timezone-information
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=False)  # Controls visibility
