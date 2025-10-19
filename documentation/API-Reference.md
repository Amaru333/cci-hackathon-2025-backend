# 📖 API Reference

Complete documentation for all API endpoints in the CCI Hackathon 2025 Backend.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format
All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": {...},
  "message": "Success message",
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error",
  "status_code": 400
}
```

---

## 🏠 General Endpoints

### Welcome Message
**GET** `/`

Returns a welcome message for the API.

**Response:**
```json
{
  "message": "Welcome to the API"
}
```

### Health Check
**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 👤 User Management

### Create User
**POST** `/users/`

Create a new user account with dietary preferences.

**Request Body:**
```json
{
  "user": "string",
  "dietary_preference": "string",
  "spice_level": "string",
  "food_allergy": ["string"],
  "daily_calorie_target": "number"
}
```

**Example:**
```json
{
  "user": "john_doe",
  "dietary_preference": "vegetarian",
  "spice_level": "medium",
  "food_allergy": ["peanuts", "shellfish"],
  "daily_calorie_target": 2000
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "message": "User created successfully",
  "user": "john_doe",
  "dietary_preference": "vegetarian",
  "spice_level": "medium",
  "food_allergy": ["peanuts", "shellfish"],
  "daily_calorie_target": 2000
}
```

**Error Responses:**
- `400` - User already exists
- `500` - Server error

### Get User
**GET** `/users/{user}`

Retrieve user profile information.

**Path Parameters:**
- `user` (string) - Username

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "user": "john_doe",
  "dietary_preference": "vegetarian",
  "spice_level": "medium",
  "food_allergy": ["peanuts", "shellfish"],
  "daily_calorie_target": 2000
}
```

**Error Responses:**
- `404` - User not found
- `500` - Server error

---

## 🧾 Receipt Processing

### Process Receipt
**POST** `/receipts/`

Upload and process a receipt image to extract item information.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload (image file)

**Supported File Types:**
- PNG
- JPG/JPEG
- GIF
- WebP

**Response:**
```json
{
  "items": [
    {
      "name": "Tomato",
      "price": 2.50,
      "quantity": 3
    },
    {
      "name": "Onion",
      "price": 1.20,
      "quantity": 2
    }
  ],
  "total": 9.90
}
```

**Error Responses:**
- `400` - Invalid file format
- `500` - AI processing error
- `500` - Perplexity API key not configured

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/receipts/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@receipt.jpg"
```

---

## 🥘 Recipe Management

### Get Personalized Recipes
**GET** `/recipes/{user}`

Generate personalized recipe suggestions based on user's available ingredients and preferences.

**Path Parameters:**
- `user` (string) - Username

**Response:**
```json
{
  "ingredients": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Tomato",
      "quantity": 5,
      "unit": "pieces",
      "user": "john_doe"
    }
  ],
  "recipes": "{\n  \"recipes\": [\n    {\n      \"recipe_name\": \"Fresh Tomato Salad\",\n      \"prep_time\": 15,\n      \"cook_time\": 0,\n      \"ingredients\": [\n        \"5 tomatoes, diced\",\n        \"1/4 cup olive oil\",\n        \"2 tbsp balsamic vinegar\",\n        \"Salt and pepper to taste\"\n      ],\n      \"steps\": [\n        \"Dice the tomatoes into bite-sized pieces\",\n        \"Whisk together olive oil and balsamic vinegar\",\n        \"Toss tomatoes with dressing\",\n        \"Season with salt and pepper\"\n      ],\n      \"feel_good_phrase\": \"Perfect for a light summer meal\",\n      \"preference_match\": \"Vegetarian-friendly and low-calorie\",\n      \"youtube\": {\n        \"title\": \"Easy Tomato Salad Recipe\",\n        \"url\": \"https://www.youtube.com/watch?v=example\"\n      }\n    }\n  ]\n}"
}
```

**Error Responses:**
- `500` - Recipe generation error
- `500` - KronosLabs API key not configured

### Add Ingredient
**POST** `/recipes/ingredients/`

Add a new ingredient to user's inventory.

**Request Body:**
```json
{
  "name": "string",
  "quantity": "number",
  "unit": "string",
  "user": "string"
}
```

**Example:**
```json
{
  "name": "Tomato",
  "quantity": 5,
  "unit": "pieces",
  "user": "john_doe"
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "message": "Ingredient added successfully",
  "name": "Tomato",
  "quantity": 5,
  "unit": "pieces",
  "user": "john_doe"
}
```

**Error Responses:**
- `500` - Database error

### Get User Ingredients
**GET** `/recipes/ingredients/{user}`

Retrieve all ingredients for a specific user.

**Path Parameters:**
- `user` (string) - Username

**Response:**
```json
{
  "user": "john_doe",
  "ingredients": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Tomato",
      "quantity": 5,
      "unit": "pieces",
      "user": "john_doe"
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "name": "Onion",
      "quantity": 2,
      "unit": "pieces",
      "user": "john_doe"
    }
  ],
  "count": 2
}
```

**Error Responses:**
- `500` - Database error

### Get All Ingredients
**GET** `/recipes/all-ingredients`

Retrieve all available ingredients from the `all_ingredients` database collection.

**Response:**
```json
{
  "ingredients": [
    {
      "name": "Country Lettuce",
      "expiry": 5,
      "category": "vegetable"
    },
    {
      "name": "Hybrid Drumstick",
      "expiry": 7,
      "category": "vegetable"
    }
  ],
  "total_count": 1000,
  "categories": [
    "baking_sweeteners",
    "canned_frozen",
    "dairy_eggs",
    "fruit",
    "grains_staples",
    "meat_seafood",
    "nuts_seeds",
    "oils_sauces",
    "snacks_beverages",
    "spices_condiments",
    "vegetable"
  ]
}
```

**Response Fields:**
- `ingredients`: Array of all available ingredients
- `total_count`: Total number of ingredients available
- `categories`: Array of unique ingredient categories

**Error Responses:**
- `404` - No ingredients found in database
- `500` - Database connection or query error

**Example cURL:**
```bash
curl "http://localhost:8000/recipes/all-ingredients"
```

---

## 📊 Data Models

### User Model
```json
{
  "user": "string",
  "dietary_preference": "string",
  "spice_level": "string",
  "food_allergy": ["string"],
  "daily_calorie_target": "number"
}
```

### Ingredient Model
```json
{
  "name": "string",
  "quantity": "number",
  "unit": "string",
  "user": "string"
}
```

### All Ingredient Model
```json
{
  "name": "string",
  "expiry": "number",
  "category": "string"
}
```

### Receipt Item Model
```json
{
  "name": "string",
  "price": "number",
  "quantity": "number"
}
```

### Recipe Response Model
```json
{
  "recipe_name": "string",
  "prep_time": "number",
  "cook_time": "number",
  "ingredients": ["string"],
  "steps": ["string"],
  "feel_good_phrase": "string",
  "preference_match": "string",
  "youtube": {
    "title": "string",
    "url": "string"
  }
}
```

---

## 🔧 Error Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

---

## 📝 Example Workflows

### Complete User Journey

1. **Create User Account**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "alice_chef",
    "dietary_preference": "vegan",
    "spice_level": "high",
    "food_allergy": ["gluten"],
    "daily_calorie_target": 1800
  }'
```

2. **Add Ingredients from Receipt**
```bash
curl -X POST "http://localhost:8000/receipts/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@grocery_receipt.jpg"
```

3. **Add Manual Ingredients**
```bash
curl -X POST "http://localhost:8000/recipes/ingredients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quinoa",
    "quantity": 1,
    "unit": "cup",
    "user": "alice_chef"
  }'
```

4. **Get Personalized Recipes**
```bash
curl "http://localhost:8000/recipes/alice_chef"
```

5. **Check User Profile**
```bash
curl "http://localhost:8000/users/alice_chef"
```

---

## 🚀 Rate Limits

Currently, there are no rate limits implemented. In production, consider implementing rate limiting to prevent abuse.

## 🔒 Security Considerations

- All file uploads are validated for type and size
- Input validation is performed on all endpoints
- Environment variables are used for sensitive configuration
- CORS is configurable for cross-origin requests

## 📱 Client SDKs

While no official SDKs are provided, the API is RESTful and can be easily integrated with any HTTP client library in any programming language.
