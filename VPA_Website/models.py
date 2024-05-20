from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

# TODO: find a way to do this in function
db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    passhash: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship()


class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped["User"] = mapped_column(ForeignKey("user.id"))

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    categories: Mapped[list["ItemCategory"]] = relationship()


class ItemCategory(db.Model):
    __tablename__ = "item_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped["Project"] = mapped_column(ForeignKey("project.id"))

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    items: Mapped[list["Item"]] = relationship()


class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped["ItemCategory"] = mapped_column(ForeignKey("item_category.id"))

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
