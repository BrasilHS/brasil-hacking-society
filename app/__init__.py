from flask import Flask

from .config import Config
from .extensions import db, migrate, ma

def create_app():
    app = Flask(
        __name__,
        template_folder="web/templates",
        static_folder="web/static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Importing database models 
    from .models import User, Post

    # Importing app routes
    from .routes.public import public_bp
    from .routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    if app.config.get("ENVIRONMENT") == "development":
        app.debug = True 

    return app

