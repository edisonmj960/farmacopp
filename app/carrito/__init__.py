from flask import Blueprint

carro = Blueprint('carro', __name__, template_folder="templates", static_folder='static')

from . import carrito