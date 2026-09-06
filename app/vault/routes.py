import json
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response,
    current_app,
)

from app.extensions import db
from app.models import User, VaultEntry
from app.security.audit import audit
from app.security.csrf import validate_csrf
from app.security.crypto import decrypt, encrypt
from app.security.passwords import generate_password, password_strength
from app.security.session_crypto import unprotect


vault_bp = Blueprint("vault", __name__, url_prefix="/vault")


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id") or not session.get("vault_key"):
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)

    return wrapper


def key():
    return unprotect(
        session["vault_key"],
        current_app.config["SECRET_KEY"]
    )


def clean(value, max_len):
    value = (value or "").strip()
    return value[:max_len]


def entry_dict(entry):
    k = key()

    return {
        "id": entry.id,
        "title": entry.title,
        "username": decrypt(entry.username_enc, k),
        "password": decrypt(entry.password_enc, k),
        "url": decrypt(entry.url_enc, k),
        "notes": decrypt(entry.notes_enc, k),
        "category": entry.category,

        # Keep these as datetime objects so Jinja can use strftime()
        "created_at": entry.created_at,
        "updated_at": entry.updated_at,
    }


@vault_bp.get("/")
@login_required
def dashboard():
    user_id = session["user_id"]

    q = clean(request.args.get("q"), 100)
    category = clean(request.args.get("category"), 50)

    entries = (
        VaultEntry.query
        .filter_by(user_id=user_id)
        .order_by(VaultEntry.updated_at.desc())
        .all()
    )

    if q:
        q_lower = q.lower()
        entries = [
            e
            for e in entries
            if q_lower in e.title.lower()
            or q_lower in e.category.lower()
        ]

    if category:
        entries = [
            e
            for e in entries
            if e.category == category
        ]

    categories = sorted(
        {
            e.category
            for e in VaultEntry.query
            .filter_by(user_id=user_id)
            .all()
        }
    )

    return render_template(
        "dashboard.html",
        entries=entries,
        categories=categories,
        q=q,
        category=category,
    )


@vault_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_entry():
    if request.method == "POST":
        if not validate_csrf(request.form.get("csrf_token")):
            return "Invalid CSRF token", 400

        title = clean(request.form.get("title"), 120)
        username = clean(request.form.get("username"), 500)
        password = request.form.get("password", "")[:5000]
        url = clean(request.form.get("url"), 1000)
        notes = request.form.get("notes", "")[:10000]
        category = clean(request.form.get("category"), 50) or "General"

        if not title or not password:
            flash("Title and password are required.")

            return (
                render_template(
                    "entry_form.html",
                    entry=None
                ),
                400,
            )

        e = VaultEntry(
            user_id=session["user_id"],
            title=title,
            username_enc=encrypt(username, key()),
            password_enc=encrypt(password, key()),
            url_enc=encrypt(url, key()),
            notes_enc=encrypt(notes, key()),
            category=category,
        )

        db.session.add(e)
        db.session.commit()

        audit(
            "vault_entry_created",
            session["user_id"]
        )

        flash("Credential saved securely.")

        return redirect(
            url_for("vault.dashboard")
        )

    return render_template(
        "entry_form.html",
        entry=None
    )


@vault_bp.route("/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    e = (
        VaultEntry.query
        .filter_by(
            id=entry_id,
            user_id=session["user_id"]
        )
        .first_or_404()
    )

    if request.method == "POST":
        if not validate_csrf(request.form.get("csrf_token")):
            return "Invalid CSRF token", 400

        e.title = clean(
            request.form.get("title"),
            120
        )

        e.username_enc = encrypt(
            clean(
                request.form.get("username"),
                500
            ),
            key()
        )

        e.password_enc = encrypt(
            request.form.get("password", "")[:5000],
            key()
        )

        e.url_enc = encrypt(
            clean(
                request.form.get("url"),
                1000
            ),
            key()
        )

        e.notes_enc = encrypt(
            request.form.get("notes", "")[:10000],
            key()
        )

        e.category = (
            clean(
                request.form.get("category"),
                50
            )
            or "General"
        )

        db.session.commit()

        audit(
            "vault_entry_updated",
            session["user_id"]
        )

        flash("Credential updated.")

        return redirect(
            url_for("vault.dashboard")
        )

    return render_template(
        "entry_form.html",
        entry=entry_dict(e)
    )


@vault_bp.post("/<int:entry_id>/delete")
@login_required
def delete_entry(entry_id):
    if not validate_csrf(request.form.get("csrf_token")):
        return "Invalid CSRF token", 400

    e = (
        VaultEntry.query
        .filter_by(
            id=entry_id,
            user_id=session["user_id"]
        )
        .first_or_404()
    )

    db.session.delete(e)
    db.session.commit()

    audit(
        "vault_entry_deleted",
        session["user_id"]
    )

    flash("Credential deleted.")

    return redirect(
        url_for("vault.dashboard")
    )


@vault_bp.get("/<int:entry_id>/view")
@login_required
def view_entry(entry_id):
    e = (
        VaultEntry.query
        .filter_by(
            id=entry_id,
            user_id=session["user_id"]
        )
        .first_or_404()
    )

    return render_template(
        "entry_view.html",
        entry=entry_dict(e)
    )


@vault_bp.get("/generate")
@login_required
def password_generator():
    try:
        length = int(
            request.args.get(
                "length",
                24
            )
        )
    except ValueError:
        length = 24

    use_symbols = (
        request.args.get(
            "symbols",
            "1"
        ) != "0"
    )

    try:
        password = generate_password(
            length,
            use_symbols
        )
    except ValueError:
        password = generate_password(
            24,
            use_symbols
        )

    return {
        "password": password,
        "strength": password_strength(password),
    }


@vault_bp.get("/export")
@login_required
def export_vault():
    import base64

    records = []

    entries = (
        VaultEntry.query
        .filter_by(
            user_id=session["user_id"]
        )
        .all()
    )

    for e in entries:
        records.append(
            {
                "id": e.id,
                "title": e.title,
                "category": e.category,

                "username_enc": base64.b64encode(
                    e.username_enc
                ).decode(),

                "password_enc": base64.b64encode(
                    e.password_enc
                ).decode(),

                "url_enc": base64.b64encode(
                    e.url_enc
                ).decode(),

                "notes_enc": base64.b64encode(
                    e.notes_enc
                ).decode(),
            }
        )

    payload = json.dumps(
        {
            "format": "securevault-encrypted-v1",
            "entries": records,
        },
        indent=2,
    )

    audit(
        "vault_exported",
        session["user_id"]
    )

    return Response(
        payload,
        mimetype="application/json",
        headers={
            "Content-Disposition": (
                "attachment; "
                "filename=securevault-encrypted-backup.json"
            ),
            "Cache-Control": "no-store",
        },
    )
