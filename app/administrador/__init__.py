from flask import Blueprint

administrador = Blueprint('administrador', __name__, template_folder="templates", static_folder='static')

from . import admin