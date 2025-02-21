from flask import Flask, render_template, request, redirect, url_for, session
import os, subprocess
from dotenv import load_dotenv

# Load credentials
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("WEB_PASSWORD", "default_secret")

def get_service_status(service):
    try:
        output = subprocess.check_output(["systemctl", "is-active", service], universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError:
        return "unknown"

@app.route("/")
def index():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", rtsp_status=get_service_status("rtsp-server"),
                           onvif_status=get_service_status("onvif-server"),
                           recording_status=get_service_status("recording-server"))

@app.route("/logs")
def logs():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    with open("/var/log/camera_status.log", "r") as log_file:
        logs = log_file.readlines()
    return render_template("logs.html", logs=logs)

@app.route("/start/<service>")
def start_service(service):
    if "logged_in" not in session:
        return redirect(url_for("login"))
    os.system(f"sudo systemctl start {service}")
    return redirect(url_for("index"))

@app.route("/stop/<service>")
def stop_service(service):
    if "logged_in" not in session:
        return redirect(url_for("index"))
    os.system(f"sudo systemctl stop {service}")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.getenv("WEB_USERNAME") and password == os.getenv("WEB_PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
