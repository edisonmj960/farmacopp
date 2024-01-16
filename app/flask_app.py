from flask import Flask, render_template, request,redirect
from flask_babel import Babel
import os
from flask_mail import Mail
from flask_mail import Mail, Message
from flask import redirect, url_for
from flask import Flask, session
from flask_session import Session
from flask_babel import gettext as _
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'

# Configuración de la extensión Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Establecer el idioma predeterminado
os.environ.setdefault('BABEL_DEFAULT_LOCALE', 'es')

babel = Babel(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Por ejemplo, aquí se usa Gmail
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'edissonmj960@gmail.com'
app.config['MAIL_PASSWORD'] = 'xjxt fuzl tvvt qtys'

mail = Mail(app)

babel = Babel(app)

@babel.localeselector
def get_locale():
    # Intenta obtener el idioma desde la sesión, si no está disponible, utiliza el mejor idioma aceptado por el navegador.
    return session.get('idioma', request.accept_languages.best_match(['es', 'en', 'de', 'fr']))


@app.route('/change-language/<lang>')
def change_language(lang):
    # Establece el idioma seleccionado en la sesión del usuario
    session['idioma'] = lang
    return redirect(url_for('cliente.index'))


from administrador import administrador
from cliente import cliente
from auth import autenticar
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from carrito import carro
from flask import make_response, jsonify
from datetime import timedelta
from os import listdir
from babel import numbers, dates
from datetime import date, datetime, time
from math import ceil


# Registro de blueprints
app.register_blueprint(administrador)
app.register_blueprint(cliente)
app.register_blueprint(autenticar)
app.register_blueprint(carro)

# Manejo de errores
error_codes = [
    400, 401, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 422, 428, 429, 431, 451, 500, 501, 502, 503, 504, 505
]
for code in error_codes:
    @app.errorhandler(code)
    def client_error(error):
        return render_template('error.html', error=error), error.code

# Configuración de Sentry
sentry_sdk.init(
    dsn="https://47b422c23c014fec8d53ccc9dc0e3e61@o4504709798952960.ingest.sentry.io/4504709801443328",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5711)
