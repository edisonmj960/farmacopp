from flask import Blueprint

cliente = Blueprint('cliente', __name__, template_folder="templates", static_folder='static')
from . import client
