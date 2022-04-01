from flask import Blueprint
from app.controllers import animies_controllers

bp = Blueprint("anime", __name__, url_prefix="/animes")

bp.get("")(animies_controllers.get_all_animes)
bp.get("/<int:id>")(animies_controllers.get_one_by_id_anime)
bp.post("")(animies_controllers.create)
bp.patch("/<int:id>")(animies_controllers.update)
bp.delete("/<int:id>")(animies_controllers.delete)