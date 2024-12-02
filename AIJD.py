import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv('google_api_key'))

# Define the Generative AI model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to start the JD-based assessment simulation
def start_jd_assessment(jd_text):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Job Description Based Assessment Simulation\n\n",
                    f"**Job Description:**\n{jd_text}\n\n"
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Welcome to the Job Description Based Assessment Simulation!\n"
                    "Please answer the following questions based on your experience and how it aligns with the provided JD."
                ],
            },
        ]
    )
    return chat_session

# Function to display JD highlights and relevant questions
def add_jd_highlights(jd_text):
    """
    This function displays the JD highlights in the sidebar
    and adds possible assessment questions.
    """
    st.sidebar.title("Job Description Highlights")
    st.sidebar.write(jd_text)

    st.sidebar.title("Assessment Questions")
    assessment_questions = [
        "1. How does your experience align with the responsibilities listed in the JD?",
        "2. Which key skills from the JD do you excel at?",
        "3. Can you share a project or experience demonstrating your fit for this role?",
        "4. What challenges do you foresee in this role, and how would you address them?",
        "5. What unique value can you bring to this position?",
    ]
    
    for question in assessment_questions:
        st.sidebar.write(question)

# Streamlit main function
def main():
    st.title("JD-Based Assessment Simulation")
    st.write("Evaluate your fit for a role by simulating an assessment based on a specific job description.")
    
    # Input for custom job description
    jd_text = st.text_area("Enter Job Description (JD):", placeholder="Paste the job description here...")

    if jd_text:
        # Add JD highlights and assessment questions to the sidebar
        add_jd_highlights(jd_text)

        # Start the JD-based assessment session
        chat_session = start_jd_assessment(jd_text)

        # User input for responses
        user_input = st.text_area("Your Response:", placeholder="Type your answer here...")
        
        if st.button("Send Response"):
            if user_input:
                with st.spinner("Processing..."):
                    response = chat_session.send_message(user_input)
                    st.subheader("AI Feedback:")
                    st.write(response.text)
            else:
                st.warning("Please enter a response before submitting.")
    else:
        st.warning("Please enter a Job Description to start the assessment.")

if __name__ == "__main__":
    main()
