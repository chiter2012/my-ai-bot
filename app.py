import streamlit as st
import google.generativeai as genai

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mening SI Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy SI Yordamchim")

# 2. Siz bergan API kalitni shu yerga joyladim
API_KEY = "AIzaSyCyYs8gwMVp5CMoDfaRABDMl_ycBbY8Q6g"
genai.configure(api_key=API_KEY)

# 3. Modelni yuklash (Eng barqaror versiya)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Suhbat xotirasi
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Oldingi xabarlarni ko'rsatish
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
            # Agar kalit bloklangan bo'lsa, xatoni ko'rsatadi
            st.error(f"Xatolik yuz berdi: {str(e)}")
            if "403" in str(e):
                st.warning("Bu kalit bloklangan ko'rinadi. Iltimos, yangi kalit oling va uni chatga yozmasdan Secrets-ga qo'ying.")
