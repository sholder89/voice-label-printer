import hmac
import sqlite3
import uuid
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)

TOKEN        = os.environ.get("LABEL_TOKEN", "changeme")
DB_PATH      = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "jobs.db"))
MAX_PENDING  = int(os.environ.get("MAX_PENDING_JOBS", "20"))
MAX_TEXT_LEN = int(os.environ.get("MAX_TEXT_LEN", "200"))

limiter = Limiter(
    get_remote_address,
    app=app,
    # Sensible defaults — IFTTT will never come close to these
    default_limits=["200 per day", "30 per hour"],
    storage_uri="memory://",
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, timeout=10)
        g.db.row_factory = sqlite3.Row
        # WAL mode allows concurrent readers + writer without blocking each other
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA synchronous=NORMAL")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS settings_changes (
                id TEXT PRIMARY KEY,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
        """)
        db.commit()


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Header only — never accept the token via query string, which would
        # write the secret into access logs. All callers (client, Lambda, Siri)
        # send the X-Token header.
        token = request.headers.get("X-Token")
        if not token or not hmac.compare_digest(token, TOKEN):
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/webhook", methods=["POST"])
@require_token
@limiter.limit("10 per minute")
def webhook():
    """IFTTT posts here. Expects JSON with value1 = label text."""
    data = request.get_json(silent=True) or {}
    text = (data.get("value1") or "").strip()

    if not text:
        return jsonify({"error": "no text provided"}), 400

    if len(text) > MAX_TEXT_LEN:
        return jsonify({"error": f"text too long (max {MAX_TEXT_LEN} characters)"}), 400

    db = get_db()

    pending = db.execute(
        "SELECT COUNT(*) FROM jobs WHERE status = 'pending'"
    ).fetchone()[0]
    if pending >= MAX_PENDING:
        return jsonify({"error": "queue full, try again later"}), 429

    job_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO jobs (id, text, status, created_at) VALUES (?, ?, 'pending', ?)",
        (job_id, text, datetime.utcnow().isoformat()),
    )
    # Keep the table lean — purge done/failed jobs older than 7 days
    db.execute(
        "DELETE FROM jobs WHERE status != 'pending' AND created_at < datetime('now', '-7 days')"
    )
    db.commit()
    return jsonify({"id": job_id, "text": text}), 201


@app.route("/jobs/pending", methods=["GET"])
@require_token
@limiter.limit("60 per minute")
def pending_jobs():
    """Local client polls this to get jobs to print."""
    db = get_db()
    rows = db.execute(
        "SELECT id, text FROM jobs WHERE status = 'pending' ORDER BY created_at"
    ).fetchall()
    return jsonify([{"id": r["id"], "text": r["text"]} for r in rows])


@app.route("/jobs/<job_id>/complete", methods=["POST"])
@require_token
def complete_job(job_id):
    db = get_db()
    db.execute("UPDATE jobs SET status = 'done' WHERE id = ?", (job_id,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/jobs/<job_id>/fail", methods=["POST"])
@require_token
def fail_job(job_id):
    db = get_db()
    db.execute("UPDATE jobs SET status = 'failed' WHERE id = ?", (job_id,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/settings", methods=["POST"])
@require_token
@limiter.limit("20 per minute")
def post_setting():
    """Lambda posts a setting change here: {key, value}."""
    VALID = {
        "font_style":   {"standard", "enhanced", "impact", "serif", "narrow", "mono", "burbank"},
        "border":       {"none", "thin", "thick", "double", "dashed", "rounded", "corners"},
        "text_case":    {"none", "uppercase", "lowercase", "title", "sentence"},
        "style_preset": {"none", "bold", "elegant", "retro", "minimal", "warning",
                          "address", "windows95", "price_tag", "cassette", "blueprint", "qr_code"},
        "font_weight":  {"normal", "bold", "italic", "bold_italic"},
        "icons":        {"true", "false"},
        "size":         {"2x1", "4x2", "4x6", "3x2", "2x0.5", "1.1x3.5", "1.1x2.4"},
    }
    data  = request.get_json(silent=True) or {}
    key   = (data.get("key")   or "").strip()
    value = (data.get("value") or "").strip().lower()

    if key not in VALID:
        return jsonify({"error": f"unknown setting '{key}'"}), 400
    if value not in VALID[key]:
        return jsonify({"error": f"invalid value '{value}' for {key}"}), 400

    db = get_db()
    change_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO settings_changes (id, key, value, status, created_at) VALUES (?, ?, ?, 'pending', ?)",
        (change_id, key, value, datetime.utcnow().isoformat()),
    )
    db.commit()
    return jsonify({"id": change_id, "key": key, "value": value}), 201


@app.route("/settings/pending", methods=["GET"])
@require_token
@limiter.limit("60 per minute")
def pending_settings():
    """Client polls this to get queued setting changes."""
    db   = get_db()
    rows = db.execute(
        "SELECT id, key, value FROM settings_changes WHERE status = 'pending' ORDER BY created_at"
    ).fetchall()
    return jsonify([{"id": r["id"], "key": r["key"], "value": r["value"]} for r in rows])


@app.route("/settings/<change_id>/complete", methods=["POST"])
@require_token
def complete_setting(change_id):
    db = get_db()
    db.execute("UPDATE settings_changes SET status = 'done' WHERE id = ?", (change_id,))
    db.commit()
    return jsonify({"ok": True})


@app.route("/health", methods=["GET"])
@limiter.exempt
def health():
    return jsonify({"ok": True})


# Run at import time so gunicorn workers also initialise the DB
with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
