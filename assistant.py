import os
from datetime import datetime
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Set environment variables
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')


class DentalClinicAssistant:
    def __init__(self, model_name: str = "llama3-70b-8192"):
        self.llm = ChatGroq(model=model_name, temperature=0.0, max_retries=2)
        self.current_date_str = datetime.now().strftime("%Y-%m-%d")
        self.current_date = datetime.strptime(self.current_date_str, "%Y-%m-%d")
        self.current_day = self.current_date.strftime("%A")
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are an AI assistant of dental clinic. You are here to provide the basic answer to their question related to dental services.
        Your task is to guide the patient through the booking process. Answer should not be more than 50 words; also add emojis wherever needed.
        Today is {current_date} ({current_day}). Clinic hours are 09:00 AM to 8:00 PM, Monday to Saturday.
        - If the user provides a date that falls on a Sunday, politely ask them to choose another day.
        - If the date is before tomorrow's date, ask the user to select a valid date.
        - Make the conversation graceful, ask for patient details one by one, and confirm the appointment with a polite response.
        - Ask if the patient needs further assistance.

        Conversation history:
        {history}

        Patient: {input}

        Assistant:
        """)
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        self.history = ""

    def book_appointment(self, user_input: str) -> str:
        response = self.chain.run(
            input=user_input,
            history=self.history,
            current_date=self.current_date_str,
            current_day=self.current_day
        )
        self.history += f"\nPatient: {user_input}\nAssistant: {response}"
        return response