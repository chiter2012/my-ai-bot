import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# API Kalitni sozlash
API_KEY = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=API_KEY)

# MAVJUD MODELLARNI AVTOMATIK ANIQLASH
@st.cache_resource
def get_working_model():
    try:
        # Avval tizimda bor bo'lgan modellarni ko'ramiz
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Eng yaxshi modellarni tartib bilan tekshiramiz
        preferred_models = [
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro', 
            'models/gemini-pro'
        ]
        
        for model_name in preferred_models:
            if model_name in available_models:
                return genai.GenerativeModel(model_name)
        
        # Agar ro'yxatdagilar topilmasa, mavjud birinchi modelni olamiz
        return genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"Modellarni yuklashda xatolik: {e}")
        return None

model = get_working_model()

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
        if model:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Javob olishda xatolik: {e}")
        else:
            st.error("Model topilmadi. API kalitni tekshiring.")
