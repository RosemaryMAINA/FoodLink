# API Endpoints

`POST /api/generate`
- body: `{ "ingredients": "rice, beans, tomato" }`
- returns: `{ "recipes": [ {title, ingredients[], steps[], estimated_cost, nutrition_score, missing_items[]} ] }`

`POST /api/save`
- body: any payload to log (e.g., selected recipe)
- returns: `{ "ok": true }`

`POST /api/payment/checkout`
- body: `{ "items": ["eggs", "flour"] }`
- returns: `{ "checkout_url": "https://..." }`

`GET /health`
- returns: `{ "status": "ok" }`
