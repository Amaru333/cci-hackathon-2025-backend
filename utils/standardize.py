import re, json
from rapidfuzz import process, fuzz

def load_inventory(filepath="constants/items.json"):
    with open(filepath, "r") as f:
        return json.load(f)

INVENTORY = load_inventory()
INVENTORY_NAMES = [item["name"].lower() for item in INVENTORY]

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    if text.endswith("es"):
        text = text[:-2]
    elif text.endswith("s"):
        text = text[:-1]
    return text.strip()

def smart_standardize(receipt_items: list, threshold: int = 80):
    """Map receipt item names to inventory names."""
    standardized = []

    for item in receipt_items:
        raw_name = item["name"]
        name = normalize(raw_name)

        if name in INVENTORY_NAMES:
            item["name"] = INVENTORY_NAMES[INVENTORY_NAMES.index(name)]
            standardized.append(item)
            continue

        matched = None
        for inv in INVENTORY_NAMES:
            if inv in name or name in inv:
                matched = inv
                break
        if matched:
            item["name"] = matched
            standardized.append(item)
            continue

        best_match, score, _ = process.extractOne(name, INVENTORY_NAMES, scorer=fuzz.token_set_ratio)
        if score >= threshold:
            item["name"] = best_match

        standardized.append(item)

    return standardized
