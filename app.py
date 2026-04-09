import streamlit as st
import re
import joblib


vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/linear_svm_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

<<<<<<< HEAD
=======

>>>>>>> 958b2b4 (commit)
def extract_links(text):
    """Extract URLs from the text"""
    return re.findall(r'http[s]?://\S+', text)

def ml_predict(message):
    """ML prediction"""
    X_vec = vectorizer.transform([message])
    pred_index = model.predict(X_vec)[0]
    label = label_encoder.inverse_transform([pred_index])[0]
    return label

def classify_message(message):
    """Final classification considering URL and ML"""
    ml_label = ml_predict(message)
    urls = extract_links(message)
    suspicious = False

    url_results = []
    for u in urls:
        if u.endswith(('.xyz', '.ru', '.top', '.click', '.info')) or any(s in u for s in ('bit.ly', 'tinyurl.com', 't.co')):
            url_results.append((u, "Fishy"))
            suspicious = True
        else:
            url_results.append((u, "Safe"))

<<<<<<< HEAD
  
=======

>>>>>>> 958b2b4 (commit)
    if suspicious and ml_label.lower() in ['ham', 'safe']:
        final_label = 'Fishy'
    else:
        final_label = ml_label

    reason = f"ML predicted '{ml_label}'"
    if final_label != ml_label:
        reason += " → Overridden due to suspicious URL"

    return final_label, reason, url_results

<<<<<<< HEAD
=======

>>>>>>> 958b2b4 (commit)
st.set_page_config(page_title="Spam / Phishing Detector", layout="centered")
st.title("📬 Spam / Fishy / Safe Detector")
st.write("Detect whether a message, email, or link is **Spam**, **Ham (Safe)**, or **Fishy**")


message_type = st.selectbox("Select type:", ["SMS", "Email", "Link (URL)"])


user_input = st.text_area(f"Enter {message_type} content:")


if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter some text!")
    else:
        result, reason, url_results = classify_message(user_input)

        
        if result.lower() in ["spam", "smishing", "phishing"]:
            st.error(f"Result: {result}")
        elif result.lower() == "fishy":
            st.warning(f"Result: {result}")
        else:
            st.success(f"Result: {result}")

        st.info(f"Reason: {reason}")

<<<<<<< HEAD
        
=======

>>>>>>> 958b2b4 (commit)
        if url_results:
            st.markdown("### 🔗 URLs detected:")
            for url, status in url_results:
                color = "#FFD700" if status=="Fishy" else "#77DD77"
                st.markdown(
                    f"<div style='padding:5px;margin-bottom:3px;background-color:{color};border-radius:5px;'>"
                    f"<a href='{url}' target='_blank' style='color:black;text-decoration:none'>{url} → {status}</a>"
                    f"</div>", unsafe_allow_html=True
                )
