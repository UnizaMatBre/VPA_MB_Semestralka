from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


def create_models(db):
    class _Namespace:
        class User(db.Model):
            id: Mapped[int] = mapped_column(primary_key=True)
            username: Mapped[str] = mapped_column(nullable=False, unique=True)
            passhash: Mapped[str] = mapped_column(nullable=False)

            projects: Mapped[list["_Namespace.Project"]] = relationship()

        class Project(db.Model):
            id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
            user_id: Mapped["_Namespace.User"] = mapped_column(ForeignKey("User.id"))

            name: Mapped[str] = mapped_column(nullable=False)
            description: Mapped[str] = mapped_column(nullable=True)

        class ItemCategory(db.Model):
            id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

            name: Mapped[str] = mapped_column(nullable=False)
            description: Mapped[str] = mapped_column(nullable=True)

    return _Namespace
