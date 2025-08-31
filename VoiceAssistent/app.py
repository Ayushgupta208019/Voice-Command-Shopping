from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import re
import spacy
import json
import os

app = Flask(__name__)
CORS(app)

# Load NLP
nlp = spacy.load("en_core_web_sm")


# Simple in-memory cart
shopping_cart = []  # each item: {id, title, price, quantity}

# --- Intent detection ---
ADD_PATTERNS = [r"\b(add|buy|purchase|include|get|want|jodo|khareedna|kharidna|chahie|lao)\b", r"\b(i\s+want\s+to\s+buy)\b"]
REMOVE_PATTERNS = [r"\b(remove|delete|discard|drop|hatao|nhi chahiye|nikalo|hta do|take\s+away)\b"]
CHECKOUT_PATTERNS = [r"\b(check\s*out|pay|place|placed|book|manga do|complete\s*order)\b"]

def detect_intent(text: str) -> str:
    t = text.lower()
    for pat in ADD_PATTERNS:
        if re.search(pat, t): return "add"
    for pat in REMOVE_PATTERNS:
        if re.search(pat, t): return "remove"
    for pat in CHECKOUT_PATTERNS:
        if re.search(pat, t): return "checkout"
    return "find"

# --- Extract item (noun keywords) ---
def extract_item(text: str):
    doc = nlp(text.lower())
    nouns = [t.text for t in doc if t.pos_ in ("NOUN","PROPN")]
    return " ".join(nouns) if nouns else text

# --- Extract quantity ---
NUM_WORDS = {
    "one":1,"two":2,"three":3,"four":4,"five":5,
    "six":6,"seven":7,"eight":8,"nine":9,"ten":10,
    "ak":1, "do":2, "teen":3, "char":4, "paach":5,
    "cah":6, "saat":7, "ath":8, "naoh":9, "dash":10
}
def extract_quantity(text: str) -> int:
    # digits
    m = re.search(r"\b(\d+)\b", text)
    if m:
        return int(m.group(1))
    # number words
    for word,num in NUM_WORDS.items():
        if re.search(rf"\b{word}\b", text.lower()):
            return num
    return 1   # default

# --- Load products from local file ---
def fetch_all_products():
    with open(os.path.join(os.path.dirname(__file__), "products.json")) as f:
        return json.load(f)

def token_overlap_score(a,b):
    A = set(re.findall(r"[a-z0-9]+", a.lower()))
    B = set(re.findall(r"[a-z0-9]+", b.lower()))
    return len(A & B)

def best_match(products, query):
    best,score=None,0
    for p in products:
        s=token_overlap_score(p.get("title",""),query)
        if s>score: best,score=p,s
    return best

# --- Routes ---
@app.route("/products", methods=["GET"])
def products_proxy():
    try:
        return jsonify({"products": fetch_all_products()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cart", methods=["GET"])
def get_cart():
    total = sum(item["price"]*item["quantity"] for item in shopping_cart)
    return jsonify({"cart": shopping_cart,"total":round(total,2)})

@app.route("/process_voice", methods=["POST"])
def process_voice():
    data=request.get_json(force=True,silent=True) or {}
    text=(data.get("text") or "").strip()
    if not text: return jsonify({"error":"No text"}),400

    action=detect_intent(text)
    item=extract_item(text)
    qty=extract_quantity(text)

    try: products=fetch_all_products()
    except Exception as e: return jsonify({"error":f"API error {e}"}),502

    if action=="add":
        match=best_match(products,item)
        if match:
            found=False
            for c in shopping_cart:
                if c["id"]==match["id"]:
                    c["quantity"]+=qty   # ✅ add multiple
                    found=True
            if not found:
                shopping_cart.append({
                    "id":match["id"],"title":match["title"],
                    "price":match["price"],"quantity":qty
                })
            return jsonify({"intent":"add","added":match["title"],"qty":qty,"cart":shopping_cart})
        return jsonify({"intent":"add","added":None,"cart":shopping_cart})

    if action=="remove":
        removed=None
        for c in shopping_cart:
            if token_overlap_score(c["title"],item)>0:
                if c["quantity"]>qty:
                    c["quantity"]-=qty
                else:
                    shopping_cart.remove(c)
                removed=c["title"]; break
        return jsonify({"intent":"remove","removed":removed,"qty":qty,"cart":shopping_cart})

    if action=="checkout":
        shopping_cart.clear()
        return jsonify({"intent":"checkout","message":"✅ Checkout successful! Your cart is now empty."})

    # find intent (suggestions)
    q=item.lower()
    suggestions=[p["title"] for p in products if q in p["title"].lower()]
    if not suggestions: suggestions=[p["title"] for p in products[:10]]
    return jsonify({"intent":"find","suggestions":suggestions})

if __name__=="__main__":
    app.run(debug=True)
