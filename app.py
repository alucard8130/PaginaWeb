
from flask import send_from_directory
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

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


@app.route("/descargas")
def descargas():
    return render_template("descargas.html")


@app.route("/tec", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        msg = Message(
            subject="Información de contacto desde la web",
            recipients=["smart8130@hotmail.com"],
            body=f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}",
        )
        try:
            mail.send(msg)
            flash("¡Mensaje enviado correctamente!", "success")
        except Exception as e:
            flash("Error al enviar el mensaje. Intenta más tarde.", "danger")
        return redirect(url_for("index"))
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def tec():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        msg = Message(
            subject="Información de contacto desde la web",
            recipients=["servicioscontablesjme@gmail.com"],
            body=f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}",
        )
        try:
            mail.send(msg)
            flash("¡Mensaje enviado correctamente!", "success")
        except Exception as e:
            flash("Error al enviar el mensaje. Intenta más tarde.", "danger")
        return redirect(url_for("tec"))
    return render_template("tec.html")


@app.route("/redes")
def redes():
    return render_template("redes.html")


@app.route("/gestor_administrativo")
def gestor_administrativo():
    return render_template("gestor_administrativo.html")


# Ruta para registro de curso
@app.route("/registro_curso", methods=["GET", "POST"])
def registro_curso():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        curso = request.form.get("curso")
        comentarios = request.form.get("comentarios")
        # Enviar correo con Flask-Mail
        msg = Message(
            subject="Nuevo registro de curso",
            recipients=["smart8130@hotmail.com"],
            body=f"Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\nCurso: {curso}\nComentarios: {comentarios}",
        )
        try:
            mail.send(msg)
            flash("¡Registro enviado correctamente!", "success")
        except Exception as e:
            flash("Error al enviar el registro. Intenta más tarde.", "danger")
    return render_template("registro_curso.html")


if __name__ == "__main__":
    app.run(debug=True)

