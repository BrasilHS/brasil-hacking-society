from ..extensions import db

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer

class Post(db.Model):

    __tablename__ = "posts" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    votes: Mapped[int] = mapped_column(Integer, default=0) 

    created_at: Mapped[int] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    ) 

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="posts"
    )
