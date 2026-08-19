"""{{FRAMEWORK}} application entry point."""

import logging

from flask import Flask
from flask import jsonify

from src.config import FLASK_PORT

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)


@app.route("/status")
def status():
    return jsonify({"status": "ok"})


def main():
    app.run(host="0.0.0.0", port=FLASK_PORT)


if __name__ == "__main__":
    main()
