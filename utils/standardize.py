import re, os
from rapidfuzz import process, fuzz
from database import get_collection

def load_inventory_from_db():
    """Load inventory from database instead of JSON file."""
    try:
        all_ingredients_collection = get_collection("all_ingredients")
        inventory = list(all_ingredients_collection.find({}))
        return inventory
    except Exception as e:
        print(f"Error loading inventory from database: {e}")
        return []

# Initialize inventory variables (will be loaded when needed)
INVENTORY = []
INVENTORY_NAMES = []

def get_inventory():
    """Get inventory data, loading from database if not already loaded."""
    global INVENTORY, INVENTORY_NAMES
    if not INVENTORY:
        INVENTORY = load_inventory_from_db()
        INVENTORY_NAMES = [item["name"].lower() for item in INVENTORY]
    return INVENTORY, INVENTORY_NAMES

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    if text.endswith("es"):
        text = text[:-2]
    elif text.endswith("s"):
        text = text[:-1]
    return text.strip()

def smart_standardize(receipt_items: list, threshold: int = None):
    """Map receipt item names to inventory names."""
    if threshold is None:
        threshold = int(os.getenv("STANDARDIZATION_THRESHOLD", "80"))
    
    # Get inventory data (lazy loading)
    inventory, inventory_names = get_inventory()
    
    standardized = []

    for item in receipt_items:
        raw_name = item["name"]
        name = normalize(raw_name)

        if name in inventory_names:
            item["name"] = inventory_names[inventory_names.index(name)]
            standardized.append(item)
            continue

        matched = None
        for inv in inventory_names:
            if inv in name or name in inv:
                matched = inv
                break
        if matched:
            item["name"] = matched
            standardized.append(item)
            continue

        best_match, score, _ = process.extractOne(name, inventory_names, scorer=fuzz.token_set_ratio)
        if score >= threshold:
            item["name"] = best_match

        standardized.append(item)

    return standardized
