from flask import Flask, render_template, request, redirect, url_for, session
import os, subprocess
from dotenv import load_dotenv

# Load credentials
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

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
                           recording_status=get_service_status("recording-server"),
                           rtsp_user=os.getenv("RTSP_USER"),
                           rtsp_pass=os.getenv("RTSP_PASS"),
                           rtsp_port=os.getenv("RTSP_PORT"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.getenv("WEB_USERNAME") and password == os.getenv("WEB_PASSWORD"):
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
