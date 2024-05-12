from VPA_Website import create_app


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

    JWT_SECRET_KEY = "test-key-please-change"
    JWT_TOKEN_LOCATION = "cookies"
    JWT_ACCESS_COOKIE_NAME = "auth_cookie"


if __name__ == "__main__":
    app = create_app(TestConfig())

    app.run()
