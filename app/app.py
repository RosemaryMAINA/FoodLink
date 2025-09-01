import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import openai

# Load .env file from parent folder
load_dotenv(dotenv_path="C:/Users/PC/Desktop/FoodLink/.env")

# Set API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
print("Loaded API Key:", openai.api_key)  # test line

app = Flask(__name__)


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SAMPLE_RECIPES_PATH = os.path.join(DATA_DIR, "sample_recipes.json")
HISTORY_PATH = os.path.join(DATA_DIR, "user_history.json")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("Loaded API Key:", openai.api_key)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
INTASEND_PUBLIC_KEY = os.getenv("INTASEND_PUBLIC_KEY")
INTASEND_SECRET_KEY = os.getenv("INTASEND_SECRET_KEY")


def _load_sample_recipes():
    with open(SAMPLE_RECIPES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_history(entry):
    history = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except Exception:
                history = []
    history.append(entry)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def generate_recipes_with_openai(ingredients_list):
    """
    Placeholder for OpenAI call. If OPENAI_API_KEY is set, you can implement the real call.
    For offline demo, we will fall back to sample recipes.
    """
    if not OPENAI_API_KEY:
        return None

    # Example schema prompt (commented out to avoid runtime errors without internet):
    # import requests
    # headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    # payload = {
    #     "model": "gpt-4o-mini",
    #     "messages": [
    #         {"role": "system", "content": "You are a recipe generator that returns simple, affordable recipes in JSON."},
    #         {"role": "user", "content": f"Given the ingredients: {', '.join(ingredients_list)}. Suggest 3 nutritious, low-cost recipes. Return JSON with fields: title, ingredients, steps (list), estimated_cost, nutrition_score (0-100), missing_items (list)."}  # noqa: E501
    #     ],
    #     "response_format": {"type": "json_object"}
    # }
    # resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
    # resp.raise_for_status()
    # data = resp.json()
    # # Extract JSON from model's response safely
    # content = data["choices"][0]["message"]["content"]
    # recipes = json.loads(content).get("recipes", [])
    # return recipes

    return None  # fallback handled by caller


def filter_sample_recipes(ingredients_list):
    """Simple filter: rank recipes by how many provided ingredients they use."""
    sample = _load_sample_recipes()
    def score(rec):
        have = set(x.strip().lower() for x in ingredients_list if x.strip())
        need = set(x.strip().lower() for x in rec.get("ingredients", []))
        return len(have & need)

    ranked = sorted(sample, key=score, reverse=True)
    return ranked[:3]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    ingredients = data.get("ingredients", "")
    ingredients_list = [x.strip() for x in ingredients.split(",") if x.strip()]
    if not ingredients_list:
        return jsonify({"error": "Please provide at least one ingredient."}), 400

    recipes = generate_recipes_with_openai(ingredients_list)
    if not recipes:
        recipes = filter_sample_recipes(ingredients_list)

    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "ingredients": ingredients_list,
        "recipes_count": len(recipes)
    }
    _save_history(entry)

    return jsonify({"recipes": recipes})


@app.route("/api/save", methods=["POST"])
def api_save():
    payload = request.get_json(silent=True) or {}
    payload["ts"] = datetime.utcnow().isoformat() + "Z"
    _save_history(payload)
    return jsonify({"ok": True})


@app.route("/api/payment/checkout", methods=["POST"])
def api_payment_checkout():
    """
    Simulate a checkout link. If IntaSend keys exist, you can implement the real call.
    For demo, we return a fake URL.
    """
    _ = request.get_json(silent=True) or {}
    fake_url = "https://pay.intasend.com/checkout/demo-FoodLink"
    return jsonify({"checkout_url": fake_url})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
