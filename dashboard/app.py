from flask import Flask, render_template, request, redirect, url_for, session
import os, subprocess
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# Load credentials
load_dotenv()

# Config validation
def validate_config():
    required_vars = ['FLASK_SECRET_KEY', 'WEB_USERNAME', 'WEB_PASSWORD']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

validate_config()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# In app configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=60)
)

# Add security headers
Talisman(app)

# Add rate limiting
limiter = Limiter(app, key_func=get_remote_address)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_service_status(service):
    allowed_services = {'rtsp-server', 'onvif-server', 'recording-server'}
    if service not in allowed_services:
        logger.warning(f"Attempted to check unauthorized service: {service}")
        return "unauthorized"
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
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Add this line
        logger.info(f"Login attempt for user: {username}")
        stored_hash = os.getenv("WEB_PASSWORD_HASH")
        if username == os.getenv("WEB_USERNAME") and check_password_hash(stored_hash, password):
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
