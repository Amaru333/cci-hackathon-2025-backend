## Byte-to-Bite Backend (FastAPI)

Backend service powering Byte-to-Bite. It provides:

- **Receipt OCR + normalization** via Perplexity AI and custom item standardization
- **User preferences** storage in MongoDB
- **Recipe generation** using KronosLabs LLM, tailored to user ingredients and preferences

Front-end repository: [Byte-to-Bite Web](https://github.com/Amaru333/byte-to-bite)

### Tech stack

- **API**: FastAPI (`main.py`, routers in `routes/`)
- **DB**: MongoDB (collections: `users`, `ingredients`)
- **OCR/Extraction**: Perplexity Chat Completions
- **LLM Recipes**: KronosLabs Chat Completions
- **Normalization**: `utils/standardize.py` with `rapidfuzz` and `constants/items.json`

## Getting started

### Prerequisites

- Python 3.10+
- MongoDB (Atlas or local)

### Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install fastapi uvicorn python-dotenv pymongo pydantic requests rapidfuzz kronoslabs
```

### Environment

Create a `.env` file in the project root with:

```bash
MONGODB_URI="mongodb+srv://<user>:<pass>@<cluster>/?retryWrites=true&w=majority"
PERPLEXITY_API_KEY="<your_perplexity_api_key>"
KRONOSLABS_API_KEY="<your_kronoslabs_api_key>"
```

### Run locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Base URLs:

- Health: `GET /health`
- Root: `GET /`

## API Reference

Base path: default (no global prefix). Routers:

- `receipts` at `/receipts`
- `recipes` at `/recipes`
- `users` at `/users`

All responses are JSON. CORS is open for development.

### Receipts

Process a receipt image to extract items and total, then normalize item names against `constants/items.json`.

- **POST** `/receipts/`
  - Content-Type: `multipart/form-data`
  - Body: `file` (image/jpeg, image/png, etc.)
  - Response 200:
    ```json
    {
      "items": [{ "name": "Tomato", "price": 1.99, "quantity": 2, "unit": "pieces" }],
      "total": 12.34
    }
    ```
  - Notes:
    - Requires `PERPLEXITY_API_KEY`
    - Normalization via `utils/standardize.smart_standardize`

Example curl:

```bash
curl -X POST http://localhost:8000/receipts/ \
  -F "file=@/path/to/receipt.jpg"
```

### Recipes

Generate 2–3 recipes based on a user’s saved ingredients and preferences.

- Mongo collections used:

  - `ingredients` documents: `{ name: str, quantity: float, unit: str, user: str }`
  - `users` documents: `{ user: str, dietary_preference: str, spice_level: str, food_allergy: [str], daily_calorie_target: float }`

- **GET** `/recipes/{user}`

  - Returns the user’s ingredients and an LLM-generated JSON string of recipes.
  - Response 200:
    ```json
    {
      "ingredients": [{ "id": "...", "name": "Tomato", "quantity": 2, "unit": "pieces", "user": "amaru" }],
      "recipes": "<JSON string with recipe objects>"
    }
    ```

- **POST** `/recipes/ingredients/`

  - Create a single ingredient for a user.
  - Body JSON:
    ```json
    { "name": "Tomato", "quantity": 2, "unit": "pieces", "user": "amaru" }
    ```
  - Response 200 includes Mongo `id`.

- **POST** `/recipes/ingredients/batch/`

  - Create multiple ingredients at once.
  - Body JSON: `[Ingredient, ...]`

- **GET** `/recipes/ingredients/{user}`

  - List a user’s ingredients (with `id`).

- **PUT** `/recipes/ingredients/{id}`

  - Update an ingredient by Mongo ObjectId.
  - Body JSON: same shape as Ingredient (all fields optional for partial update behavior as implemented).

- **DELETE** `/recipes/ingredients/{id}`

  - Delete an ingredient by Mongo ObjectId.

- **POST** `/recipes/custom-prompt`
  - Like `GET /recipes/{user}` but provides an additional custom prompt.
  - Body JSON:
    ```json
    { "user": "amaru", "prompt": "High-protein breakfast" }
    ```

Notes:

- Requires `MONGODB_URI` and `KRONOSLABS_API_KEY`
- The `recipes` field in responses is a JSON string from the LLM; parse it in the client if needed

Example curl (list ingredients):

```bash
curl http://localhost:8000/recipes/ingredients/amaru
```

### Users

Create and fetch user preference profiles.

- **POST** `/users/`

  - Body JSON:
    ```json
    {
      "user": "amaru",
      "dietary_preference": "vegetarian",
      "spice_level": "medium",
      "food_allergy": ["peanuts"],
      "daily_calorie_target": 2000
    }
    ```
  - Errors: 400 if user already exists

- **GET** `/users/{user}`
  - Returns the stored user document with `id`.

Example curl (create user):

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": "amaru",
    "dietary_preference": "vegetarian",
    "spice_level": "medium",
    "food_allergy": ["peanuts"],
    "daily_calorie_target": 2000
  }'
```

## Configuration details

- `constants/items.json`: canonical inventory names and rough expiry days used for name matching.
- `utils/standardize.py`:
  - `normalize(text)`: lowercases, strips punctuation, handles plural endings.
  - `smart_standardize(items, threshold=80)`: exact/substring/fuzzy matching via `rapidfuzz`.

## Development tips

- Start MongoDB first and verify `MONGODB_URI` connectivity.
- If Perplexity returns non-JSON text, the endpoint attempts a fallback parsing; failures return 500 with a helpful message.
- CORS is wide-open for local development via `CORSMiddleware` in `main.py`.

## Running tests

(No tests included yet.) Consider adding FastAPI route tests and Mongo fixtures.

## Deployment

- Expose with a production ASGI server (e.g., `uvicorn` workers behind a reverse proxy).
- Set environment variables securely in your platform (e.g., Docker/K8s/Render/Vercel functions).

## License

MIT (or project default)
