import os
import re
import joblib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
MODEL_PATH = os.path.join("model", "cybershield_model.pkl")

# Transparent, editable keyword list. These are indicators, not proof.
HARMFUL_TERMS = {
    "insult": ["idiot", "stupid", "loser", "worthless", "pathetic", "useless"],
    "threat": ["hurt you", "kill you", "threaten", "make your life miserable"],
    "harassment": ["keep bothering", "keep insulting", "nobody likes you",
                   "nobody wants you", "go away"]
}

def find_indicators(message):
    text = message.lower()
    found = []
    categories = []
    for category, terms in HARMFUL_TERMS.items():
        matches = [term for term in terms if term in text]
        if matches:
            categories.append(category)
            found.extend(matches)
    return sorted(set(found)), sorted(set(categories))

def analyse_message(message):
    model = joblib.load(MODEL_PATH)
    prediction = int(model.predict([message])[0])
    probabilities = model.predict_proba([message])[0]
    bullying_probability = float(probabilities[1])

    terms, categories = find_indicators(message)

    # Combine model and transparent keyword signals conservatively.
    if "threat" in categories:
        risk = "High"
    elif prediction == 1 or categories:
        risk = "Medium"
    else:
        risk = "Low"

    flagged = prediction == 1 or bool(terms)
    if "threat" in categories:
        explanation = "A possible threat-related phrase was found. Take it seriously, but review the full context."
    elif terms:
        explanation = "Potentially harmful wording was found. Context is important before deciding whether this is bullying."
    elif prediction == 1:
        explanation = "The demo ML model found patterns associated with bullying."
    else:
        explanation = "No listed harmful indicators were found and the demo model did not flag the text."

    recommendations = []
    if flagged:
        recommendations = [
            "If this sender is repeatedly harassing you, consider using the platform's block controls.",
            "Use the platform's report option if the message violates its rules.",
            "If you may need to report it, keep relevant evidence such as the message, date and sender details.",
            "Review account privacy and message-request settings."
        ]
    else:
        recommendations = [
            "No action may be needed based on this scan.",
            "If the message still makes you uncomfortable, you can mute, block or report it using the platform's controls.",
            "Review privacy settings and limit messages from unknown accounts."
        ]

    return {
        "status": "Potential bullying indicators found" if flagged else "No clear bullying indicators found",
        "flagged": flagged,
        "risk": risk,
        "confidence": round(bullying_probability * 100, 1),
        "harmful_terms": terms,
        "categories": categories,
        "explanation": explanation,
        "recommendations": recommendations,
        "privacy": "Message is analysed in this app process and is not saved to a database."
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyse", methods=["POST"])
def analyse():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message to scan."}), 400
    if len(message) > 5000:
        return jsonify({"error": "Message is too long. Maximum 5000 characters."}), 400

    try:
        result = analyse_message(message)
        return jsonify(result)
    except FileNotFoundError:
        return jsonify({"error": "Model not found. Run train_model.py first."}), 500

if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        print("Training model first...")
        import train_model
    app.run(debug=False, host="127.0.0.1", port=5000)
