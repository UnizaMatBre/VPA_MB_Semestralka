from sqlalchemy.orm import Mapped, mapped_column


def create_models(db):
    class _Namespace:
        class User(db.Model):
            id: Mapped[int] = mapped_column(primary_key=True)
            username: Mapped[str] = mapped_column(nullable=False, unique=True)
            passhash: Mapped[str] = mapped_column(nullable=False)


    return _Namespace
