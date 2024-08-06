import os
import streamlit as st
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_community.callbacks.manager import get_openai_callback

# Ensure this script can be run standalone by setting up the environment
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

# Accessing env variables using getenv
key = os.getenv("OPENAI_API_KEY")

if not key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Calling OpenAI with model and API key
try:
    llm = ChatOpenAI(openai_api_key=key, model='gpt-4', temperature=0.8)
except Exception as e:
    raise RuntimeError(f"Failed to initialize OpenAI model: {e}")

# First Chain
TEMPLATE1 = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. \
Make sure the questions are not repeated and check all the questions to be conforming the text as well. \
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=['text', 'number', 'subject', 'tone', 'response_json'],
    template=TEMPLATE1
)

# Using RunnableSequence
chain1 = quiz_generation_prompt | llm

# Second Chain
TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. \
If the quiz is not up to par with the cognitive and analytical abilities of the students,\
update the quiz questions that need to be changed and adjust the tone such that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=['quiz', 'subject'],
    template=TEMPLATE2
)

# Using RunnableSequence
chain2 = quiz_evaluation_prompt | llm

# Constructing the final sequence
FinalChain = chain1 | chain2

