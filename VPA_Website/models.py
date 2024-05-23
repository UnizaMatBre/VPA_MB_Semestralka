from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

# TODO: find a way to do this in function
db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    passhash: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")


class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    owner: Mapped["User"] = relationship(back_populates="projects")

    categories: Mapped[list["ItemCategory"]] = relationship(back_populates="my_project")


class ItemCategory(db.Model):
    __tablename__ = "item_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    my_project: Mapped["Project"] = relationship(back_populates="categories")

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    items: Mapped[list["Item"]] = relationship(back_populates="category")


class Item(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("item_category.id"))

    category: Mapped["ItemCategory"] = relationship(back_populates="items")

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
