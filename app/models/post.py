from ..extensions import db

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer

class Post(db.Model):

    __tablename__ = "posts" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    votes: Mapped[int] = mapped_column(Integer, default=0) 

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    ) 

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    ) 

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="posts"
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def set_user_id(self, user_id):
        self.user_id = user_id
