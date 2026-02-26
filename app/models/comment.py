from ..extensions import db

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer

class Comment(db.Model):

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
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

    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    post: Mapped["Post"] = relationship(
        back_populates="comments"
    )

    parent_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comments.id"),
        nullable=True
    )

    user_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="comments"
    )

    replies: Mapped[list["Comment"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    parent: Mapped["Comment"] = relationship(
        remote_side=[id],
        back_populates="replies"
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

