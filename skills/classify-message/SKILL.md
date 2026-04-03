---
name: classify-message
description: "Classifies SMS, Email, and Links using ML model + URL rules"
allowed-tools: Bash Read Write
---

# Classify Message Skill

Instructions:

1. Accept input: message text, type (SMS/Email/Link)
2. Preprocess message: lowercase, remove unnecessary punctuation
3. Extract URLs
4. Load trained ML model:
   - linear_svm_model.pkl
   - tfidf_vectorizer.pkl
   - label_encoder.pkl
5. Predict ML label (Spam / Ham / Offensive)
6. Apply URL rules:
   - suspicious domain (.xyz, .ru, .top)
   - shortened links (bit.ly, tinyurl.com)
   - If ML predicts Ham but URL is suspicious → override to Fishy
7. Output JSON:
```json
{
  "result": "Spam/Fishy/Safe",
  "reason": "Brief explanation why"
}


---

# **Step 3️⃣: Add Python Skill Logic (Optional)**

Save as `skills/classify-message/skill.py` if backend Python API needed:

```python
import pickle, re

# Load models
vectorizer = pickle.load(open("models/tfidf_vectorizer.pkl","rb"))
model = pickle.load(open("models/linear_svm_model.pkl","rb"))
label_encoder = pickle.load(open("models/label_encoder.pkl","rb"))

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

def ml_predict(message):
    X_vec = vectorizer.transform([message])
    pred_index = model.predict(X_vec)[0]
    label = label_encoder.inverse_transform([pred_index])[0]
    return label

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

# Example usage
msg = "You won a prize! Click http://bit.ly/abc"
print(classify_message(msg))