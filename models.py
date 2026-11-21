"""SQLAlchemy models for registered devices and observed monitoring history."""

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now():
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    date_added = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False)
    last_status = db.Column(db.String(20), nullable=False, default="unknown")
    last_checked = db.Column(db.DateTime(timezone=True))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    checks = db.relationship(
        "MonitoringCheck", back_populates="device", cascade="all, delete-orphan"
    )
    events = db.relationship(
        "ConnectivityEvent", back_populates="device", cascade="all, delete-orphan"
    )


class MonitoringCheck(db.Model):
    __tablename__ = "monitoring_checks"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)
    response_time_ms = db.Column(db.Float)
    checked_at = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    error_message = db.Column(db.String(500))

    device = db.relationship("Device", back_populates="checks")


class ConnectivityEvent(db.Model):
    __tablename__ = "connectivity_events"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False, index=True)
    previous_status = db.Column(db.String(20), nullable=False)
    new_status = db.Column(db.String(20), nullable=False)
    event_time = db.Column(db.DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    description = db.Column(db.String(255))

    device = db.relationship("Device", back_populates="events")
