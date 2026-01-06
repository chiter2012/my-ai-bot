import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# API kalitni xavfsiz olish
# Avval Streamlit Secrets'dan qidiradi, topilmasa vaqtincha koddan oladi
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"

if not api_key:
    st.error("API kalit topilmadi. Iltimos, Secrets sozlamasini tekshiring!")
    st.stop()

genai.configure(api_key=api_key)

# 404 xatoligini oldini olish uchun barqaror model nomi
# Agar flash ishlamasa, avtomatik ravishda pro versiyaga o'tadi
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    model = genai.GenerativeModel('gemini-pro')

# Suhbat tarixini saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixdagi xabarlarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Foydalanuvchi kiritishi
if prompt := st.chat_input("Savolingizni yozing..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # SI javobi
    with st.chat_message("assistant"):
        try:
            # Modelga xabar yuborish
            response = model.generate_content(prompt)
            bot_text = response.text
            st.markdown(bot_text)
            st.session_state.messages.append({"role": "assistant", "content": bot_text})
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
