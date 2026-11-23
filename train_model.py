import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Small demonstration dataset only.
# Replace/expand with a carefully reviewed, diverse, labelled dataset
# before treating predictions as reliable.
data = [
    ("Have a nice day", 0),
    ("You did a great job", 0),
    ("Thank you for helping me", 0),
    ("You are a good friend", 0),
    ("I appreciate your work", 0),
    ("Let's study together", 0),
    ("That was really helpful", 0),
    ("Hope you are doing well", 0),
    ("You are welcome here", 0),
    ("I disagree with your opinion", 0),
    ("Please stop messaging me", 0),
    ("I don't like this behaviour", 0),
    ("I think your answer is incorrect", 0),
    ("Can we talk about this later", 0),
    ("Please respect my boundaries", 0),
    ("You are stupid and useless", 1),
    ("Nobody likes you", 1),
    ("You are worthless", 1),
    ("I will hurt you", 1),
    ("Everyone should hate you", 1),
    ("You are a complete idiot", 1),
    ("I will make your life miserable", 1),
    ("Stop being such a loser", 1),
    ("You deserve to be bullied", 1),
    ("I am going to threaten you", 1),
    ("Nobody wants you around", 1),
    ("You are pathetic", 1),
    ("Go away nobody wants you", 1),
    ("You are annoying and useless", 1),
    ("I will keep insulting you", 1),
    ("I will embarrass you online", 1),
    ("You should be ashamed of yourself", 1),
]

X = [row[0] for row in data]
y = [row[1] for row in data]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ))
])

pipeline.fit(X, y)
os.makedirs("model", exist_ok=True)
joblib.dump(pipeline, "model/cybershield_model.pkl")
print("Model trained and saved: model/cybershield_model.pkl")
print("Note: this is a small demo model, not a validated safety classifier.")
