from ..extensions import db
from ..utils.security import hash_password, verify_password

from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime

from argon2 import PasswordHasher, Type

ph = PasswordHasher(
    memory_cost=65536,      # 64 MiB de memória
    time_cost=4,            # 4 iterações
    parallelism=2,          # 2 threads
    hash_len=32,            # Tamanho do hash: 32 bytes
    type=Type.ID            # Usa Argon2id
)

class User(db.Model):

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid4().hex)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False) 
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

    def insert(self):
        try:    
            self.password = hash_password(self.password)
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def check_password(self, password):
        return verify_password(self.password, password)
    