import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# Sizning API kalitingiz
API_KEY = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=API_KEY)

# 404 muammosini hal qiluvchi mantiq
# Biz 'models/gemini-1.5-flash-latest' nomini ishlatamiz, bu v1beta uchun eng mosidir
@st.cache_resource
def load_model():
    # Birinchi bo'lib eng yangi flash modelini sinaymiz
    try:
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        # Agar u bo'lmasa, pro versiyasini sinaymiz
        return genai.GenerativeModel('gemini-pro')

model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            st.error(f"Xatolik: {str(e)}")
            st.info("Maslahat: API kalitingiz Google AI Studio-da 'Active' ekanligini tekshiring.")
