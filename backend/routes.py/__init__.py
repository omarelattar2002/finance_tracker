from flask import Flask
from backend.config import Config
from backend.extensions import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    mongo.init_app(app)

    from .users import users_bp
    from .budgets import budgets_bp
    from .transactions import transactions_bp



    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(budgets_bp, url_prefix="/budgets")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")

    return app
