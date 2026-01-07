import streamlit as st
import google.generativeai as genai

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# 2. API Kalitni sozlash (Siz bergan kalit)
API_KEY = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=API_KEY)

# 3. Modelni tanlash (404 xatosini bermaydigan eng yangi variant)
# Biz 'gemini-1.5-flash-latest' nomidan foydalanamiz
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
            st.error(f"Xatolik yuz berdi: {str(e)}")
