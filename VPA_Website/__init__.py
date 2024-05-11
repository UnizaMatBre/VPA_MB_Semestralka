from flask import Flask, render_template


class Localization:
    def __getitem__(self, name):
        return name

def create_app(app_config):
    app = Flask(__name__)


    app.config.from_object(app_config)


    # load localization (implement translations
    localization = Localization()

    from models import create_models
    models = create_models(None)

    @app.route("/")
    @app.route("/index")
    def index_get():
        return render_template("index.html", localization=localization)

    return app
