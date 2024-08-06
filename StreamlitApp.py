import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcq_gen.utils import read_file, get_table_data
from src.mcq_gen.mcqgenerator import chain1, chain2  # Import chains separately
from src.mcq_gen.logger import logging

# Correct the file path
with open(r'E:\GENAI\MCQ-GEN\response.json', 'r') as file:
    RESPONSE_JSON = file.read()  # Read as a raw JSON string

st.title("MCQ GENERATOR APPLICATION")

with st.form("user_inputs"):
    # File upload
    uploaded_file = st.file_uploader("Enter a pdf file or txt file")

    # Input fields
    mcq_count = st.number_input("No of MCQs", min_value=3, max_value=50, step=1)

    # Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity of Questions", max_chars=20, placeholder="Simple")

    # Add button
    button = st.form_submit_button("Create MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    try:
        text = read_file(uploaded_file)
        # Tracing tokens (token count, cost, i/p tokens, o/p tokens etc)
        with get_openai_callback() as cb:
            # Prepare inputs as a dictionary or other required format
            inputs = {
                'text': text,
                'number': mcq_count,
                'subject': subject,
                'tone': tone,
                'response_json': RESPONSE_JSON  # Pass as raw JSON string
            }
            
            # Generate quiz
            quiz_response = chain1.invoke(input=inputs)

            # Print quiz_response to inspect its structure
            st.write(f"Quiz Response: {quiz_response}")

            # Check if the response contains 'content'
            if hasattr(quiz_response, 'content'):
                # Use the raw JSON string directly
                quiz_json_str = quiz_response.content

                # Use get_table_data function to format quiz_json_str
                table_data = get_table_data(quiz_json_str)
                
                # Check if table_data is not None
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index = df.index + 1  # Adjust index to start from 1
                    st.table(df)
                else:
                    st.error("Error in table data")
            else:
                raise ValueError("No content found in the quiz response.")

            # Evaluate quiz
            evaluation_inputs = {
                'quiz': quiz_json_str,  # Use the raw JSON string for evaluation
                'subject': subject
            }
            response = chain2.invoke(input=evaluation_inputs)

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        st.error(f"Error: {str(e)}")
    else:
        st.write(f"Total Cost: {cb.total_cost}")
        st.write(f"Total Tokens: {cb.total_tokens}")
        st.write(f"Input Tokens: {cb.prompt_tokens}")
        st.write(f"Output Tokens: {cb.completion_tokens}")

        if isinstance(response, dict):
            quiz = response.get("quiz", None)
            if quiz is not None:
                # Use the raw JSON string for displaying in table
                table_data = get_table_data(quiz)
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index = df.index + 1
                    st.table(df)
                    st.text_area("Review", value=response.get("review", ""))
                else:
                    st.error("Error in table data")
