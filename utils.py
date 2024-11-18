#display chat messages in Streamlit
def display_chat(messages):
    
    import streamlit as st

    for msg in messages:
        if msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])
        else:
            st.chat_message("user").write(msg["content"])