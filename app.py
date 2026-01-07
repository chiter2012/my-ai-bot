import streamlit as st
from openai import OpenAI

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Mening ChatGPT Botim", page_icon="🤖")
st.title("🤖 Mening Shaxsiy ChatGPT Yordamchim")

# 2. Yangi OpenAI API kalitingizni shu yerga joyladim
API_KEY = "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"

client = OpenAI(api_key=API_KEY)

# 3. Suhbat xotirasini yaratish
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Oldingi xabarlarni ekranga chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Savol-javob mantiqi
if prompt := st.chat_input("ChatGPT-dan so'rang..."):
    # Foydalanuvchi xabari
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ChatGPT javobi
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xatolik yuz berdi: {str(e)}")
            if "insufficient_quota" in str(e):
                st.warning("Eslatma: OpenAI hisobingizda mablag' (balans) bo'lishi kerak.")
