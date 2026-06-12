from flask import send_from_directory
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
import json,os
from dotenv import load_dotenv
from datetime import datetime
from flask import request, jsonify
from functools import wraps
from flask import session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Ruta para servir ads.txt desde la raíz
@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(".", "ads.txt")


app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.live.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)


# Cambia esta contraseña por una segura
ADMIN_PASSWORD =os.getenv("ADMIN_PASSWORD")
#app.secret_key = 'una_clave_secreta_larga_y_aleatoria'  # si no tienes ya una

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged'):
            return redirect(url_for('admin_login', next=request.path))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged'] = True
            return redirect(request.args.get('next') or '/admin/testimonios')
        error = 'Contraseña incorrecta'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect('/admin/login')


# @app.route("/descargas")
# def descargas():
#     return render_template("descargas.html")


# @app.route("/tec", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         nombre = request.form["nombre"]
#         email = request.form["email"]
#         mensaje = request.form["mensaje"]

#         msg = Message(
#             subject="Información de contacto desde la web",
#             recipients=["smart8130@hotmail.com"],
#             body=f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}",
#         )
#         try:
#             mail.send(msg)
#             flash("¡Mensaje enviado correctamente!", "success")
#         except Exception as e:
#             flash("Error al enviar el mensaje. Intenta más tarde.", "danger")
#         return redirect(url_for("index"))
#     return render_template("index.html")


@app.route("/")
def tec():
    return render_template("index.html")


# @app.route("/redes")
# def redes():
#     return render_template("redes.html")


@app.route("/gestor_administrativo")
def gestor_condominal():
    return render_template("gestor_administrativo.html")

#beta testers
@app.route("/beta")
def beta():
    return render_template("beta.html")


#descargas
@app.route("/descargas")
def descargas():
    return render_template("descarga_app.html")

#mantpro
@app.route("/mantpro_app")
def mantpro():
    return render_template("mantpro.html")


# Ruta para política de privacidad GESAC Condóminos
@app.route('/politica_privacidad_gesac_condominos')
def politica():
    return render_template('politica_privacidad_gesac_condominos.html')

#ruta para index.html
# @app.route("/index")
# def index_page():
#     return render_template("index.html")
TESTIMONIOS_FILE = 'testimonios.json'

def leer_testimonios():
    if not os.path.exists(TESTIMONIOS_FILE):
        return []
    with open(TESTIMONIOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_testimonios(data):
    with open(TESTIMONIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Recibir nuevo testimonio
@app.route('/testimonios/nuevo', methods=['POST'])
def nuevo_testimonio():
    data = request.get_json()
    testimonios = leer_testimonios()
    testimonios.append({
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'nombre': data.get('nombre', '').strip(),
        'rol': data.get('rol', '').strip(),
        'texto': data.get('texto', '').strip(),
        'fecha': datetime.now().strftime('%d/%m/%Y'),
        'aprobado': False
    })
    guardar_testimonios(testimonios)
    return jsonify({'ok': True})

# Panel de moderación — protégelo con una ruta secreta
@app.route('/admin/testimonios')
@login_required
def admin_testimonios():
    testimonios = leer_testimonios()
    return render_template('admin_testimonios.html', testimonios=testimonios)

# Aprobar
@app.route('/admin/testimonios/aprobar/<id>', methods=['POST'])
@login_required
def aprobar_testimonio(id):
    testimonios = leer_testimonios()
    for t in testimonios:
        if t['id'] == id:
            t['aprobado'] = True
    guardar_testimonios(testimonios)
    return jsonify({'ok': True})

# Eliminar
@app.route('/admin/testimonios/eliminar/<id>', methods=['POST'])
@login_required
def eliminar_testimonio(id):
    testimonios = leer_testimonios()
    testimonios = [t for t in testimonios if t['id'] != id]
    guardar_testimonios(testimonios)
    return jsonify({'ok': True})

# Testimonios aprobados (para cargarlos en la página)
@app.route('/testimonios/aprobados')
def testimonios_aprobados():
    testimonios = leer_testimonios()
    aprobados = [t for t in testimonios if t['aprobado']]
    return jsonify(aprobados)


if __name__ == "__main__":
    app.run(debug=True)
