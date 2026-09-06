from flask import Flask, redirect, render_template, session, url_for
from config import Config
from .extensions import db, limiter
from .security.csrf import csrf_token


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    limiter.init_app(app)

    from .auth.routes import auth_bp
    from .vault.routes import vault_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)

    @app.context_processor
    def inject_security_helpers():
        return {"csrf_token": csrf_token}

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
        return response

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("vault.dashboard"))
        return render_template("index.html")

    return app
