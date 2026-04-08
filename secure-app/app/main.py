import os
from typing import Any

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

MAX_MESSAGE_LENGTH = 200


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Limit request body to 16 KB.

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.post("/api/v1/echo")
    def echo() -> tuple[dict[str, Any], int]:
        try:
            payload = request.get_json(force=False, silent=False)
        except BadRequest:
            return {"error": "Invalid JSON body"}, 400

        if not isinstance(payload, dict):
            return {"error": "JSON object expected"}, 400

        message = payload.get("message")
        if not isinstance(message, str):
            return {"error": "'message' must be a string"}, 400

        cleaned = message.strip()
        if not cleaned:
            return {"error": "'message' cannot be empty"}, 400

        if len(cleaned) > MAX_MESSAGE_LENGTH:
            return {
                "error": f"'message' exceeds max length of {MAX_MESSAGE_LENGTH}"
            }, 400

        return jsonify({"message": cleaned, "length": len(cleaned)}), 200

    return app


app = create_app()


if __name__ == "__main__":
    # Debug is disabled by default for safer local runs.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
