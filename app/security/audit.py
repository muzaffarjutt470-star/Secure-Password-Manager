from flask import request
from app.extensions import db
from app.models import AuditEvent


def audit(action, user_id=None):
    db.session.add(AuditEvent(action=action, user_id=user_id, ip_address=request.remote_addr))
    db.session.commit()
