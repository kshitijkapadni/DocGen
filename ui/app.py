import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="DocGen.AI MVP")
st.title("📝 DocGen MVP")

chat_history = []

# Save chat
def save_chat(chat):
    os.makedirs("chat_store", exist_ok=True)
    with open("chat_store/session.json", "w") as f:
        json.dump(chat, f)

# Load chat
def load_chat():
    try:
        with open("chat_store/session.json", "r") as f:
            return json.load(f)
    except:
        return []

chat_history = load_chat()

# Input
user_input = st.text_input("You:", key="input")
if user_input:
    chat_history.append({"sender": "user", "message": user_input})
    save_chat(chat_history)

# Display chat
for chat in chat_history:
    st.write(f"**{chat['sender']}**: {chat['message']}")

# Doc generation
if st.button("📄 Generate Document"):
    description = chat_history[0]["message"] if chat_history else "No description provided"
    resp = requests.post("http://localhost:8001/generate-doc", json={"description": description, "chat": chat_history})
    if resp.status_code == 200:
        st.download_button("Download .docx", resp.content, file_name="documentation.docx")
    else:
        st.error("Failed to generate document")
