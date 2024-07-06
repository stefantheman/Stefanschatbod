#----User Authenticator----
import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Stefan Pappas"]
usernames = ["SPappas27"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticator(names, usernames, hashed_passwords, "sales_dashboard", "friends27", cookie_expiry_days=2)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")


if authentication_status:
    #----logout----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    #----Open AI Code----
    from openai import OpenAI
    import streamlit as st
    
    client = OpenAI()
    
    st.title("Stefan's Time Management AI Assistant")
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a time managment assistant. You help students manage their time and let them know when they have assignments due."}]
    
    for message in st.session_state.messages:
        if message ["role"] != "system":
          with st.chat_message(message["role"]):
              st.markdown(message["content"])
    
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.chat_message("assistant"):
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
