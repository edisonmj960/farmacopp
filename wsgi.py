import sys
import os

# Añade la ruta de tu proyecto al path de PythonAnywhere
sys.path.append("/home/usuario/mi_proyecto")

# Configura la variable de entorno para tu aplicación Flask
os.environ["FLASK_APP"] = "app"

# Activa tu virtualenv
activate_this = '/home/usuario/.virtualenvs/mi_entorno_virtual/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Importa tu aplicación Flask
from Farmacop import app as application