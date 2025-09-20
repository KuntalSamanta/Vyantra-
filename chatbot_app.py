import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import base64
import random
import datetime

# -------------------- CONFIG --------------------
load_dotenv(".env")
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()
# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Vyantra - Your AI Friend",
    page_icon="logo.png",
    layout="centered"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
        font-family: 'Poppins', sans-serif;
    }
    .chat-bubble-user {
        background: #DCF8C6;
        color: black;
        padding: 12px;
        border-radius: 18px;
        margin: 6px 0;
        text-align: right;
        max-width: 85%;
        margin-left: auto;
        word-wrap: break-word;
    }
    .chat-bubble-bot {
        background: #F1F0F0;
        color: #003366;
        padding: 12px;
        border-radius: 18px;
        margin: 6px 0;
        text-align: left;
        max-width: 85%;
        margin-right: auto;
        word-wrap: break-word;
    }
    small {
        color: gray;
        font-size: 11px;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 12px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- LOGO LOADER --------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file("logo.png")

# -------------------- HEADER WITH ANIMATED LOGO --------------------
st.markdown(
    f"""
    <style>
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}
    .animated-logo {{
        animation: pulse 2.5s infinite;
    }}
    </style>

    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 15px;'>
        <img src="data:image/png;base64,{logo_base64}" width="100" class="animated-logo" style="margin-right:10px;">
        <h1 style='margin: 0; color:#2e7d32;'>Vyantra</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------- SIDEBAR --------------------
st.sidebar.image("logo.png", width=160)
st.sidebar.markdown("<div style='margin-bottom:5px;'></div>", unsafe_allow_html=True)
st.sidebar.title("About Vyantra")
st.sidebar.write("🌱 *Vyantra* is your personal AI mental health companion.")
st.sidebar.write("It provides **stress support**, **motivational guidance**, and a safe space to chat.")
st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Developed by **Kuntal Samanta**")
st.sidebar.write("📌 *The mantra of life breath*")

# -------------------- DAILY QUOTE --------------------
quotes = [
    "“Calm mind brings inner strength and self-confidence.” – Dalai Lama",
    "“Happiness depends upon ourselves.” – Aristotle",
    "“Every day may not be good… but there’s something good in every day.”",
    "“Give yourself the same care and attention you give to others.”",
    "“The greatest weapon against stress is our ability to choose one thought over another.” – William James",
    "“You yourself, as much as anybody in the entire universe, deserve your love and affection.” – Buddha",
    "“Do not let the behavior of others destroy your inner peace.” – Dalai Lama",
    "“What lies behind us and what lies before us are tiny matters compared to what lies within us.” – Ralph Waldo Emerson",
    "“Peace comes from within. Do not seek it without.” – Buddha",
    "“Keep your face always toward the sunshine—and shadows will fall behind you.” – Walt Whitman",
    "“The mind is everything. What you think you become.” – Buddha",
    "“Start where you are. Use what you have. Do what you can.” – Arthur Ashe",
    "“The present moment is the only time over which we have dominion.” – Thích Nhất Hạnh",
    "“Believe you can and you're halfway there.” – Theodore Roosevelt",
    "“When you arise in the morning think of what a privilege it is to be alive, to think, to enjoy, to love…” – Marcus Aurelius",
    "“The best way to predict your future is to create it.” – Abraham Lincoln",
    "“Don’t count the days, make the days count.” – Muhammad Ali",
    "“Inhale the future, exhale the past.”",
    "“You are stronger than you think and more capable than you know.”",
    "“One small positive thought in the morning can change your whole day.”"
]

st.success(random.choice(quotes))

# -------------------- CHAT HISTORY --------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display messages (normal flow, no fixed window)
for role, text, ts in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {text}<br><small>{ts}</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>Vyantra:</b> {text}<br><small>{ts}</small></div>", unsafe_allow_html=True)

# -------------------- SYSTEM PRE-COMMAND --------------------
pre_command = """
You are Vyantra, a mental health support chatbot designed to help students 
with stress, anxiety, motivation, and general mental well-being. 
Your role is to provide emotional support, coping strategies, 
and gentle consultation for mental health.

Rules:
1. Only answer questions related to mental health and student well-being.  
2. If the user asks about anything unrelated (like coding, math, random facts, etc.), 
   politely reply: "⚕️ I am a medical chatbot created to support mental health, so I cannot provide an answer to that."  
3. If the user asks a mental health-related question but you don’t know the answer, 
   reply: "🙏 I may not have the right answer for this. Please consider consulting our doctor for proper guidance."  
4. Always be empathetic, encouraging, and supportive in tone.
"""

# # Send pre-command as the first system message
# chat.send_message(pre_command)


# -------------------- USER INPUT --------------------
# Start chat only once and send pre_command once
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    st.session_state.chat.send_message(pre_command)

user_input = st.chat_input("Type your message...")
if user_input:
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state["messages"].append(("user", user_input, timestamp))

    response = st.session_state.chat.send_message(user_input)
    bot_reply = response.text
    st.session_state["messages"].append(("bot", bot_reply, timestamp))

    st.rerun()

# -------------------- FOOTER --------------------
st.markdown('<div class="footer">© 2025 Vyantra | The mantra of life breath</div>', unsafe_allow_html=True)

