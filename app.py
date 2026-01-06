import streamlit as st
import google.generativeai as genai

# 1. Sahifa dizayni va sarlavhasi
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")
st.markdown("Google Gemini 1.5 Flash yordamida ishlaydi.")

# 2. API Kalitni xavfsiz olish
# Streamlit Secrets'dan qidiradi, topilmasa kod ichidagi zahira kalitni ishlatadi
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyC2T1kkG2_Q15CeUlk_5SbCugJsNrN1GBY"
genai.configure(api_key=api_key)

# 3. Gemini modelini sozlash (Eng barqaror versiya qo'shildi)
# 'gemini-1.5-flash-latest' versiyasi 404 xatoligini oldini oladi
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 4. Suhbat tarixini saqlash uchun xotira
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Avvalgi xabarlarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Savol-javob mantiqi
if prompt := st.chat_input("Savolingizni bu yerga yozing..."):
    # Foydalanuvchi xabarini xotiraga qo'shish
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot javobini olish
    with st.chat_message("assistant"):
        try:
            # SI dan javob generatsiya qilish
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # Bot javobini xotiraga qo'shish
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
            st.info("Eslatma: API kalitingiz yoki model versiyasi bilan muammo bo'lishi mumkin.")
