from VPA_Website import create_app


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


if __name__ == "__main__":
    app = create_app(TestConfig())

    app.run()
