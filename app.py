import streamlit as st
import google.generativeai as genai

# 1. Sahifa dizaynini sozlash
st.set_page_config(
    page_title="Mening SI Botim", 
    page_icon="🤖", 
    layout="centered"
)

st.title("🤖 Mening Shaxsiy SI Yordamchim")
st.markdown("Google Gemini API asosida ishlovchi aqlli chatbot.")

# 2. API Kalitni xavfsiz tekshirish
# Streamlit Secrets-dan kalitni oladi
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Agar Secrets sozlanmagan bo'lsa, o'zingizning kalitingizni vaqtincha ishlatadi
    api_key = "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"

genai.configure(api_key=api_key)

# 3. Modelni yuklash (Gemini 1.5 Flash - tezkor va aqlli)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Suhbat tarixini (xotirani) saqlash
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Avvalgi xabarlarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Foydalanuvchidan savol qabul qilish
if prompt := st.chat_input("Savolingizni bu yerga yozing..."):
    # Foydalanuvchi xabarini xotiraga qo'shish
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot javobini generatsiya qilish
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # SI dan javob olish
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Bot javobini xotiraga qo'shish
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
