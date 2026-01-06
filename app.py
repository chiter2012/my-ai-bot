import streamlit as st
import google.generativeai as genai

# 1. Sahifa ko'rinishi
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# 2. API Kalitni sozlash
# Avval Streamlit Secrets'dan qidiradi, bo'lmasa koddagi zahira kalitni oladi
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=api_key)

# 3. Modelni yuklash (Siz so'ragan 'gemini-pro' versiyasi)
# Bu versiya 404 xatoligini bermasligi kerak
model = genai.GenerativeModel('gemini-pro')

# 4. Suhbat tarixini (chat xotirasini) saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Avvalgi xabarlarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Savol-javob mantiqi
if prompt := st.chat_input("Savolingizni yozing..."):
    # Foydalanuvchi xabarini xotiraga qo'shish
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot javobini olish
    with st.chat_message("assistant"):
        try:
            # SI dan javob generatsiya qilish
            response = model.generate_content(prompt)
            bot_text = response.text
            st.markdown(bot_text)
            
            # Bot javobini xotiraga qo'shish
            st.session_state.messages.append({"role": "assistant", "content": bot_text})
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
            st.info("Maslahat: API kalit to'g'riligini va internet aloqasini tekshiring.")
