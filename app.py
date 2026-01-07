import streamlit as st
import google.generativeai as genai

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# 2. API Kalitni sozlash
API_KEY = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=API_KEY)

# 3. Modelni tanlash (404 xatosini bermasligi uchun eng sodda nomni yozamiz)
# Agar 'gemini-1.5-flash' xato bersa, tizim 'gemini-pro' ga o'tadi
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = genai.GenerativeModel('gemini-pro')

# 4. Suhbat xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Xabarlarni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Savol-javob mantiqi
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # SI dan javob olish
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar model topilmasa, boshqa model bilan qayta urinib ko'ramiz
            st.error("Model ulanishida xatolik. Qayta urinib ko'rilmoqda...")
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
