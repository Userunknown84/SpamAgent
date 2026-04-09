# 📬 Spam Detection AI Agent

This project is an **AI-powered Spam Detection Agent** that classifies **SMS, Emails, and Links (URLs)** as **Spam, Fishy, or Safe**. It uses a **Machine Learning model** trained on text data along with **URL heuristics** to flag suspicious links.

---

## 🧩 Features

- Classify **SMS**, **Email**, or **Links (URLs)**.
- Detect suspicious domains (`.xyz`, `.ru`, `.top`, `.click`, `.info`) and shortened URLs (`bit.ly`, `tinyurl.com`, `t.co`).
- Explain why a message was flagged (`ML predicted` + `URL check`).
- Built with **Python, FastAPI, and Streamlit**.
- Safe: Does not store any user data.

---

## 🗂️ Project Structure
spam-agent/
├── models/ # ML models
│ ├── tfidf_vectorizer.pkl
│ ├── linear_svm_model.pkl
│ └── label_encoder.pkl
├── skills/ # Optional AI skill logic
│ └── classify-message/
│ └── skill.py
├── api.py # FastAPI backend
├── app.py # Streamlit frontend
├── rules.md # Project rules
├── agentsoul.md # Agent identity / soul
├── README.md


---

## ⚙️ Requirements

Python 3.13 or above.  

**Python packages:**

```bash
pip install fastapi==0.116.1 uvicorn==0.35.0 scikit-learn==1.7.1 joblib==1.5.1 pydantic==2.11.7 streamlit==1.28.0

🚀 Running the Agent

1️⃣ FastAPI Backend

uvicorn api:app --reload

2️⃣ Streamlit Frontend

streamlit run app.py

🔧 How it Works
Input Preprocessing – Lowercase, remove unnecessary punctuation.
URL Extraction – Detect URLs in the message.
ML Prediction – Uses LinearSVC + TFIDF Vectorizer.
URL Rules – Suspicious / short links override ham → Fishy.
Output – Returns JSON with result and reason.

\
