from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Necesario para flash

# Configuración de Flask-Mail (ejemplo con Hotmail)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.live.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def index():
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
        return redirect(url_for("index"))
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/contacto")
# def contact():
#    return render_template("contacto.html")


@app.route("/tec", methods=["GET", "POST"])
def tec():
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
        return redirect(url_for("tec"))
    return render_template("tec.html")


if __name__ == "__main__":
    app.run(debug=True)
