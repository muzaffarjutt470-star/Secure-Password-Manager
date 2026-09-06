from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from app.extensions import db, limiter
from app.models import User
from app.security.audit import audit
from app.security.csrf import validate_csrf
from app.security.crypto import derive_key, new_salt
from app.security.session_crypto import protect
from app.security.passwords import hash_master_password, verify_master_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def valid_username(username):
    return 3 <= len(username) <= 80 and username.replace("_", "").replace("-", "").isalnum()


def valid_master_password(password):
    return len(password) >= 12


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not validate_csrf(request.form.get("csrf_token")):
            return "Invalid CSRF token", 400
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not valid_username(username):
            flash("Username must be 3–80 letters/numbers, '_' or '-'.")
            return render_template("register.html"), 400
        if not valid_master_password(password):
            flash("Master password must be at least 12 characters.")
            return render_template("register.html"), 400
        user = User(username=username, password_hash=hash_master_password(password), salt=new_salt())
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username is already registered.")
            return render_template("register.html"), 409
        audit("account_created", user.id)
        flash("Account created. Please sign in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if request.method == "POST":
        if not validate_csrf(request.form.get("csrf_token")):
            return "Invalid CSRF token", 400
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if not user or not verify_master_password(user.password_hash, password):
            audit("login_failed", user.id if user else None)
            flash("Invalid username or password.")
            return render_template("login.html"), 401
        session.clear()
        session.permanent = True
        session["user_id"] = user.id
        session["vault_key"] = protect(derive_key(password, user.salt), __import__("flask").current_app.config["SECRET_KEY"])
        audit("login_success", user.id)
        return redirect(url_for("vault.dashboard"))
    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    if not validate_csrf(request.form.get("csrf_token")):
        return "Invalid CSRF token", 400
    user_id = session.get("user_id")
    if user_id:
        audit("logout", user_id)
    session.clear()
    return redirect(url_for("index"))
