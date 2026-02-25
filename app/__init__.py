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
    from .models import User, Post, Comment

    # Importing api routes
    from .api.auth import auth_api_bp
    from .api.post import post_api_bp
    app.register_blueprint(auth_api_bp, url_prefix="/api/auth")
    app.register_blueprint(post_api_bp, url_prefix="/api/post")

    # Importing views routes
    from .views.auth import auth_view_bp
    from .views.public import public_bp
    from .views.post import post_view_bp
    app.register_blueprint(auth_view_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(post_view_bp, url_prefix="/post")

    if app.config.get("ENVIRONMENT") == "development":
        app.debug = True 

    return app

