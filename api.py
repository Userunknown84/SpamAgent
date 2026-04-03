from fastapi import FastAPI
from pydantic import BaseModel
import joblib, re

# Load models
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/linear_svm_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# URL extraction & flagging
def extract_links(text):
    return re.findall(r'http[s]?://\S+', text)

def url_flag(message):
    urls = extract_links(message)
    suspicious_domains = ('.xyz', '.ru', '.top')
    short_links = ('bit.ly', 'tinyurl.com')
    for u in urls:
        if u.endswith(suspicious_domains) or any(s in u for s in short_links):
            return True
    return False

# ML prediction
def ml_predict(message):
    X_vec = vectorizer.transform([message])
    pred_index = model.predict(X_vec)[0]
    label = label_encoder.inverse_transform([pred_index])[0]
    return label

# Final classification
def classify_message(message):
    ml_label = ml_predict(message)
    if url_flag(message) and ml_label == 'ham':
        final_label = 'Fishy'
    else:
        final_label = ml_label
    reason = f"ML predicted '{ml_label}'"
    if final_label != ml_label:
        reason += " → Overridden due to suspicious URL"
    return {"result": final_label, "reason": reason}

# FastAPI setup
app = FastAPI(title="Spam Detection API")

class Message(BaseModel):
    text: str

@app.post("/classify")
def classify(msg: Message):
    return classify_message(msg.text)

@app.get("/")
def root():
    return {"message": "Spam Detection API Running!"}