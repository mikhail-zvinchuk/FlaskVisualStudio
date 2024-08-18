from flask import Flask, request, render_template, abort
import os
import openaihandler as oh
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)

try:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key")
    openai_handler = oh.OpenAIHandler(api_key=api_key)
except Exception as e:
    logging.error(f"Failed to initialize OpenAIHandler: {str(e)}")
    raise


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post():
    try:
        original_text = request.form.get("text")
        target_language = request.form.get("language")

        translated_text = openai_handler.translate_text(original_text, target_language)

        return render_template(
            "results.html",
            translated_text=translated_text,
            original_text=original_text,
            target_language=target_language,
        )
    except Exception as e:
        logging.error(f"Error during translation: {str(e)}")
        return render_template(
            "error.html",
            error_message="An error occurred during translation. Please try again.",
        )


if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "5555"))
    except ValueError:
        logging.warning("Invalid port number. Defaulting to 5555.")
        PORT = 5555

    logging.info(f"Starting server on {HOST}:{PORT}")
    app.run(HOST, PORT)
