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
from psycopg import connect
from psycopg.rows import dict_row


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


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





@app.route("/")
def tec():
    return render_template("index.html")





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
# TESTIMONIOS_FILE = 'testimonios.json'

# def leer_testimonios():
#     if not os.path.exists(TESTIMONIOS_FILE):
#         return []
#     with open(TESTIMONIOS_FILE, 'r', encoding='utf-8') as f:
#         return json.load(f)

# def guardar_testimonios(data):
#     with open(TESTIMONIOS_FILE, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL no está configurada. Configúrala para usar Supabase.")
    return connect(DATABASE_URL, sslmode="require", row_factory=dict_row)


def init_testimonios_table():
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS testimonios (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    rol TEXT NOT NULL,
                    texto TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    aprobado BOOLEAN NOT NULL DEFAULT FALSE
                    )
                    """
                )
    finally:
        conn.close()


init_testimonios_table()



# Recibir nuevo testimonio
@app.route('/testimonios/nuevo', methods=['POST'])
def nuevo_testimonio():
    data = request.get_json() or {}
    nombre = data.get('nombre', '').strip()
    rol = data.get('rol', '').strip()
    texto = data.get('texto', '').strip()

    if not nombre or not rol or not texto:
        return jsonify({'ok': False, 'error': 'Datos incompletos'}), 400

    nuevo_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    fecha = datetime.now().strftime('%d/%m/%Y')

    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO testimonios (id, nombre, rol, texto, fecha, aprobado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (nuevo_id, nombre, rol, texto, fecha, False)
                )
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/admin/testimonios')
@login_required
def admin_testimonios():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nombre, rol, texto, fecha, aprobado
                FROM testimonios
                ORDER BY id DESC
                """
            )
            testimonios = cur.fetchall()
        conn.close()
        return render_template('admin_testimonios.html', testimonios=testimonios)
    except Exception as e:
        return f"Error cargando testimonios: {e}", 500


@app.route('/admin/testimonios/aprobar/<id>', methods=['POST'])
@login_required
def aprobar_testimonio(id):
    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE testimonios SET aprobado = TRUE WHERE id = %s",
                    (id,)
                )
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/admin/testimonios/eliminar/<id>', methods=['POST'])
@login_required
def eliminar_testimonio(id):
    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM testimonios WHERE id = %s",
                    (id,)
                )
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/testimonios/aprobados')
def testimonios_aprobados():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nombre, rol, texto, fecha, aprobado
                FROM testimonios
                WHERE aprobado = TRUE
                ORDER BY id DESC
                """
            )
            aprobados = cur.fetchall()
        conn.close()
        return jsonify(aprobados)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
