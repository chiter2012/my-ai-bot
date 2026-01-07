import streamlit as st
from openai import OpenAI

# Sahifa sozlamalari
st.set_page_config(page_title="ChatGPT Bot", page_icon="🤖")
st.title("🤖 Mening ChatGPT Botim")

# 1. API Kalitni sozlash (OpenAI kalitini kiriting)
# Streamlit Secrets-dan OPENAI_API_KEY ni qidiradi
api_key = st.secrets.get("OPENAI_API_KEY") or "BU_YERGA_OPENAI_KALITINI_QOYING"

client = OpenAI(api_key=api_key)

# 2. Suhbat xotirasi
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Tarixni ko'rsatish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Savol-javob mantiqi
if prompt := st.chat_input("ChatGPT-dan so'rang..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ChatGPT-ga so'rov yuborish
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xatolik: {str(e)}")
