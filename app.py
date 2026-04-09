import streamlit as st
import re
import joblib


try:
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    model = joblib.load("models/linear_svm_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")
except:
    st.error("Model files not found! Please ensure 'models/' folder has the required files.")
    st.stop()

def extract_links(text):
    """Extract URLs from the text"""
    return re.findall(r'http[s]?://\S+', text)

def ml_predict(message):
    """Predict label using ML model"""
    X_vec = vectorizer.transform([message])
    pred_index = model.predict(X_vec)[0]
    label = label_encoder.inverse_transform([pred_index])[0]
    return label

def classify_message(message, message_type):
    """Final classification based on message type"""

    
    ml_label = ml_predict(message).lower()
    if ml_label in ['ham', 'safe', 'not spam']:
        ml_label = 'Safe'
    elif ml_label in ['spam', 'phishing', 'smishing']:
        ml_label = 'Spam'

    
    if message_type == "Link (URL)":
        urls = [message.strip()]
        suspicious = False
        url_results = []

        suspicious_keywords = ['login', 'verify', 'update', 'bank', 'secure', 'account']

        for u in urls:
            if (
                u.endswith(('.xyz', '.ru', '.top', '.click', '.info')) or
                any(s in u for s in ('bit.ly', 'tinyurl.com', 't.co')) or
                any(k in u.lower() for k in suspicious_keywords)
            ):
                url_results.append((u, "Fishy"))
                suspicious = True
            else:
                url_results.append((u, "Safe"))

        final_label = "Fishy" if suspicious else "Safe"
        reason = "URL-based detection"

        return final_label, reason, url_results

   
    else:
        final_label = ml_label
        reason = f"ML predicted '{ml_label}'"
        return final_label, reason, []


st.set_page_config(page_title="Spam / Fishy / Safe Detector", layout="centered")
st.title("📬 Spam / Fishy / Safe Detector")
st.write("Detect whether a message, email, or link is **Spam**, **Safe**, or **Fishy**")

message_type = st.selectbox("Select type:", ["SMS", "Email", "Link (URL)"])
user_input = st.text_area(f"Enter {message_type} content:")

if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter some text!")
    else:
        result, reason, url_results = classify_message(user_input, message_type)

        
        if result.lower() in ["spam", "smishing", "phishing"]:
            st.error(f"Result: {result}")
        elif result.lower() == "fishy":
            st.warning(f"Result: {result}")
        else:
            st.success(f"Result: {result}")

        st.info(f"Reason: {reason}")

        if url_results:
            st.markdown("### 🔗 URLs detected:")
            for url, status in url_results:
                color = "#FFD700" if status=="Fishy" else "#77DD77"
                st.markdown(
                    f"<div style='padding:5px;margin-bottom:3px;background-color:{color};border-radius:5px;'>"
                    f"<a href='{url}' target='_blank' style='color:black;text-decoration:none'>{url} → {status}</a>"
                    f"</div>", unsafe_allow_html=True
                )