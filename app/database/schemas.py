from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, String, LargeBinary, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserSchema(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    email_address: Mapped[str] = mapped_column(String(50))
    full_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str]
    gender: Mapped[str] = mapped_column(String(25))
    programming_stack: Mapped[str]
    date_responded: Mapped[datetime] = mapped_column(insert_default=func.now())

    certificates: Mapped[List["CertificateSchema"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"email={self.email_address}, full name = {self.full_name}"


class CertificateSchema(Base):
    __tablename__ = "certificate"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(150))
    file_data: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["UserSchema"] = relationship(back_populates="certificates")

    def __repr__(self) -> str:
        return f"cetificate_name={self.file_name}"
