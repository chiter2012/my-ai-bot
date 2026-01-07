import streamlit as st
import google.generativeai as genai

# Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# API Kalitni sozlash (Siz bergan kalit)
API_KEY = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=API_KEY)

# 404 XATOSINI YO'QOTISH USULI:
# Model nomini 'models/' prefiksi bilan to'liq yozamiz
# Bu Google API-ga aynan qaysi modelni ishlatishni aniq ko'rsatadi
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Suhbat xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Xabarlarni ko'rsatish
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
            # SI dan javob olish
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("SI javob qaytara olmadi. Qayta urinib ko'ring.")
                
        except Exception as e:
            # Agar model topilmasa, zahira modelga o'tish
            st.error(f"Xatolik: {str(e)}")
            st.info("Zahira modelga (gemini-pro) ulanishga harakat qilinmoqda...")
            try:
                backup_model = genai.GenerativeModel('models/gemini-pro')
                response = backup_model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Hozirda Google xizmatlarida ulanish muammosi mavjud.")
