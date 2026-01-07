import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# API Kalitni sozlash
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=api_key)

# 404 xatoligini to'liq yo'qotish uchun model nomini to'liq yozamiz
# Agar gemini-pro topilmasa, gemini-1.5-flash-latest ni sinaymiz
try:
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Suhbat xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Savol-javob mantiqi
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
