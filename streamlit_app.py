import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="🤗💬 История")

with st.sidebar:
    st.title('🤗💬 HugChat - История')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('Учетные данные для входа в HuggingFace уже предоставлены!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Введите e-mail:', type="default")
        hf_pass = st.text_input('Введите пароль:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Пожалуйста, введите свои учетные данные!', icon='⚠️')
        else:
            st.success('Перейдите к вводу сообщения.!', icon='👉')

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Чем я могу вам помочь?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    pr = f"Это: {prompt_input} - вопрос. Если вопрос не по истории не отвечай. Предложи что ты любиш истории и не интересует остальное. только отвечай на русском языке"
    return chatbot.chat(pr)

if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
