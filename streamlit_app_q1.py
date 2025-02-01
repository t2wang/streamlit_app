import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

groqChat = ChatGroq(temperature=0.9, groq_api_key="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", model_name="llama-3.3-70b-versatile")

prompt = PromptTemplate(
    input_variables=["inquiry"],
    template="""
    You are a customer support chatbot for XYZ Dealership. Based on the customer's inquiry, determine the correct department they should contact. 
    The departments are:
    - Sales
    - Car Service
      - Emergency
      - General Maintenance
    - Human Resources
    - Other
    
    Respond only with the department and (if applicable) sub-department name. 
    
    Inquiry: {inquiry}
    Response:
    """
)

llmChain = LLMChain(llm=groqChat, prompt=prompt)

# Streamlit UI
st.title("XYZ Dealership Chatbot")
st.write("Ask about services at XYZ Dealership, and I'll direct you to the right department!")

inquiry = st.text_input("Enter your inquiry:")
if st.button("Submit"):
    if inquiry:
        response = llmChain.run(inquiry=inquiry)
        st.write("### Department:")
        st.write(response)
    else:
        st.warning("Please enter an inquiry.")
