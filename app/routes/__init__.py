from flask import Blueprint, Flask
from .animies_routes import bp as bp_animies

bp_app = Blueprint("api", __name__, url_prefix="")

def init_app(app: Flask):
    bp_app.register_blueprint(bp_animies)
    app.register_blueprint(bp_app)