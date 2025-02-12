from __future__ import annotations

from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):  # type: ignore
    pass  # Inherit from DeclarativeBase


class Schema(Base):
    __tablename__ = "schemas"

    id: Mapped[str] = mapped_column(primary_key=True)
    data_items: Mapped[list[Data]] = relationship(back_populates="schema")
    schema: Mapped[str] = mapped_column(TEXT, nullable=False)


class Data(Base):
    __tablename__ = "data"

    id: Mapped[str] = mapped_column(primary_key=True)
    id_schema: Mapped[str] = mapped_column(
        ForeignKey("schemas.id")
    )  # Type-annotated, ForeignKey
    schema: Mapped[Schema] = relationship(back_populates="data_items")
