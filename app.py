import streamlit as st
import google.generativeai as genai

# 1. Sahifa dizayni
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# 2. API Kalitni xavfsiz olish
# Avval Streamlit Secrets'dan qidiradi, bo'lmasa koddagi zahira kalitni oladi
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=api_key)

# 3. Modelni sozlash (404 xatosini oldini olish uchun eng barqaror versiya)
# 'gemini-1.5-flash' o'rniga 'gemini-1.5-flash-latest' ishlatamiz
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 4. Suhbat xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Tarixni ko'rsatish
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
