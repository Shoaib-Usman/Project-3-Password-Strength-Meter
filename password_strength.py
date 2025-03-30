import streamlit as st
import re
import string
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Secure Password Tool",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
    <style>
        .stApp { background-color: #f4f4f4; }
        .css-card { 
            background: white; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
            margin-bottom: 20px;
        }
        .password-display {
            background-color: #eef2ff;
            border-radius: 6px;
            padding: 10px;
            font-family: monospace;
            text-align: center;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ""

st.title("🔐 Secure Password Strength Meter & Generator")

# Function to generate a password
def generate_password(length, upper, lower, digits, special):
    chars = ""
    if lower:
        chars += string.ascii_lowercase
    if upper:
        chars += string.ascii_uppercase
    if digits:
        chars += string.digits
    if special:
        chars += string.punctuation
    
    return "".join(random.choice(chars) for _ in range(length)) if chars else "Please select character types"

# Password Strength Checker Section
st.markdown("### 📊 Check Password Strength")
password = st.text_input("Enter your password:", type="password")

if password:
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
        feedback.append("Make your password at least 12 characters long.")
    else:
        feedback.append("Your password is too short. Use at least 8 characters.")
    
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        feedback.append("Add uppercase letters for better security.")
    
    if re.search(r'[a-z]', password):
        score += 15
    else:
        feedback.append("Include lowercase letters.")
    
    if re.search(r'\d', password):
        score += 15
    else:
        feedback.append("Use numbers to strengthen your password.")
    
    if re.search(r'[' + re.escape(string.punctuation) + ']', password):
        score += 15
    else:
        feedback.append("Add special characters like !@#$%^&*.")
    
    strength_levels = [(80, "Strong", "#16a34a"), (60, "Moderate", "#facc15"), (30, "Weak", "#f97316"), (0, "Very Weak", "#dc2626")]
    strength, color = next((s, c) for t, s, c in strength_levels if score >= t)
    
    st.markdown(f"**Password Strength:** <span style='color:{color}; font-weight:600;'>{strength}</span>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for i in range(score + 1):
        progress_bar.progress(i / 100)
        time.sleep(0.005)
    
    if feedback:
        st.markdown("**Improve Your Password:**")
        for item in feedback:
            st.write(f"- {item}")

# Password Generator Section
st.markdown("### 🔑 Generate a Secure Password")
length = st.slider("Password Length", 8, 32, 16)
upper = st.checkbox("Include Uppercase Letters", True)
lower = st.checkbox("Include Lowercase Letters", True)
digits = st.checkbox("Include Numbers", True)
special = st.checkbox("Include Special Characters", True)

if st.button("Generate Password"):
    generated_password = generate_password(length, upper, lower, digits, special)
    st.session_state.generated_password = generated_password
    st.markdown(f"**Generated Password:**")
    st.markdown(f"<div class='password-display'>{generated_password}</div>", unsafe_allow_html=True)
