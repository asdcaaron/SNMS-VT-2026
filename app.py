"""Flask application entry point for SNMS-VT-2026."""

from pathlib import Path

from flask import Flask, jsonify, render_template
from sqlalchemy import func, text

from models import ConnectivityEvent, Device, MonitoringCheck, db


def create_app(config_object="config.Config"):
    """Create the Flask app and initialize its local SQLite database."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    # Importing the model classes above registers their tables with SQLAlchemy.

    # Models will be imported here as they are added, so create_all can
    # discover them without creating a fabricated database or sample results.
    with app.app_context():
        db.create_all()

    @app.get("/")
    def dashboard():
        """Render the initial dashboard using actual database records."""
        stats = {
            "total_devices": Device.query.count(),
            "online_devices": Device.query.filter_by(last_status="online").count(),
            "no_response_devices": Device.query.filter_by(last_status="no_response").count(),
            "unknown_devices": Device.query.filter_by(last_status="unknown").count(),
            "average_response_ms": db.session.query(
                func.avg(MonitoringCheck.response_time_ms)
            ).filter(
                MonitoringCheck.status == "online",
                MonitoringCheck.response_time_ms.is_not(None),
            ).scalar(),
        }
        recent_devices = Device.query.order_by(Device.device_name.asc()).limit(100).all()
        recent_events = ConnectivityEvent.query.order_by(
            ConnectivityEvent.event_time.desc()
        ).limit(10).all()
        return render_template(
            "dashboard.html", stats=stats, recent_devices=recent_devices,
            recent_events=recent_events
        )

    @app.get("/health")
    def health():
        """Report healthy only when a real SQLite query succeeds."""
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({
                "application": "SNMS-VT-2026",
                "status": "running",
                "database": "connected",
            }), 200
        except Exception:
            app.logger.exception("Database health check failed")
            db.session.rollback()
            return jsonify({
                "application": "SNMS-VT-2026",
                "status": "error",
                "database": "disconnected",
            }), 503

    return app


app = create_app()


if __name__ == "__main__":
    # Bind to localhost only; do not expose the prototype to a wider network.
    app.run(host="127.0.0.1", port=5000, debug=True)
