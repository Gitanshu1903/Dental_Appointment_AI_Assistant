import streamlit as st
from assistant import DentalClinicAssistant
from utils import display_chat


def main():
    st.title("Dental Clinic Assistant 🦷")
    st.write("Welcome! Ask me about our dental services or book an appointment. 😊")

    # assistant and chat history
    if "assistant" not in st.session_state:
        st.session_state.assistant = DentalClinicAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! 😊 How can I assist you today?"}]

    # Display conversation history
    display_chat(st.session_state.messages)

    # Input from user
    user_input = st.chat_input("Type your message here...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # response from assistant
        assistant = st.session_state.assistant
        response = assistant.book_appointment(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)


if __name__ == "__main__":
    main()