# FoodLink – AI-Powered Recipe & Nutrition Recommender (Zero Hunger)

Turn what's in your kitchen into nutritious meals. Built for **Vibe Coding 4-3-2 Hackathon** (SDG 2: Zero Hunger).

## ✨ What it does
- Input ingredients → get 3 simple, low-cost recipes
- See a basic nutrition score, steps, and missing items
- Simulate checkout for missing items (IntaSend-ready)
- Store user history locally (JSON) – can be swapped to Supabase

## 🧠 AI
- Uses OpenAI (optional). If `OPENAI_API_KEY` is not set, the app falls back to curated sample recipes for an **offline-safe demo**.

## 🧱 Stack
- Frontend: HTML/CSS/JS (vanilla)
- Backend: Python (Flask)
- Data: JSON (demo) – swap to Supabase/MySQL easily
- Payments: IntaSend (stubbed)

## 🚀 Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Copy env file and fill keys if you have them
cp .env.example .env  # Windows: copy .env.example .env

# Run
python app/app.py
# Open http://localhost:5000
```

## 🔐 Environment variables (.env)

```
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
INTASEND_PUBLIC_KEY=
INTASEND_SECRET_KEY=
```

If no keys are provided, the app still works using `/data/sample_recipes.json`.

## 📦 Deployment
- Easiest path: containerize or run via Bolt.new/Render/Heroku.
- Ensure `PORT` is set by the platform. The app reads `PORT` env var.

## 📁 Project structure
```
FoodLink/
  app/
    app.py
    static/
      app.js
      style.css
    templates/
      index.html
  data/
    sample_recipes.json
    user_history.json
  docs/
    pitch_deck.md
    submission_checklist.md
    api_endpoints.md
    testing_plan.md
    judging_map.md
  tests/
    test_basic.md
  requirements.txt
  .env.example
  README.md
  LICENSE
```

## 🧪 Testing
See `docs/testing_plan.md`. Basic manual tests + placeholder automated test file.

## 👥 Team (add yourselves)
- Name – Role – Email
```
