from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import fitz
from prompt import *

# Load environment variables from the .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Plagiarism  function checker
def plagiarism(input_text):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002", temperature=1, api_key=GOOGLE_API_KEY)
    PROMPT_TEMPLATE =PROMPT
    prompt = PromptTemplate(
        input_variables=["input_text"], # From prompt
        template=PROMPT_TEMPLATE,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response=llm_chain.run({"input_text":input_text})
    return response


# Streamlit App Configuration
st.set_page_config(page_title="Plagiarism Checker", layout="wide")
st.header("Plagiarism Checker")

# File upload or text input
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    try:
        # Read and extract text using PyMuPDF (fitz)
        pdf_text = ""
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in pdf_document:
            pdf_text += page.get_text()
        pdf_document.close()

        user_input = pdf_text
        st.text_area("Extracted Text from PDF", user_input, height=200)
    except Exception as e:
        st.error(f"Failed to process the uploaded PDF: {e}")
else:
    user_input = st.text_area("Enter your text", height=200)


# Generate Plagarism check
if st.button("Start Checking"):
    response=plagiarism(input_text=user_input)
    st.write(response)

    
