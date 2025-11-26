import streamlit as st
import os
from agent import create_agent_executor

# --- Page Configuration ---
st.set_page_config(
    page_title="Retail AI Agent",
    page_icon="🤖",
    layout="wide"
)

# --- Header ---
st.title("Retail AI Agent for Inventory Demand Forecast 🤖")
st.subheader("Your intelligent assistant for demand forecasting and inventory recommendations.")

# --- Sidebar for Instructions and Warnings ---
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1.  **Ask a question** about demand forecasts or inventory in the text box.
    2.  Click the **'Generate Report'** button.
    3.  The agent will analyze the data and provide a detailed explanation and recommendation.
    """)

    st.warning("""
    **Important:** Before starting, ensure that:
    1.  You have Ollama installed and running.
    2.  You have pulled a model (e.g., `ollama pull mistral`).
    3.  The `sales.csv` and `inventory.csv` files exist (run `python data_generator.py` if not).
    """, icon="⚠️")
    
    st.info("The agent's thought process will be printed to the terminal where you launched Streamlit.", icon="ℹ️")


# --- Main Application ---
st.markdown("### Ask the Agent")

# Pre-defined example questions
example_questions = [
    "What is the demand forecast for Product A for the next 30 days, and should we reorder?",
    "Which product had the highest sales last month?",
    "Compare the sales of Product B and Product C in the last quarter.",
    "Give me a full inventory report and identify which items might need reordering soon based on recent sales trends.",
]
selected_question = st.selectbox("Choose an example question or type your own below:", options=example_questions, index=0)

# User input text area
user_question = st.text_area("Your question:", value=selected_question, height=100)

# Generate Report button
if st.button("Generate Report", type="primary"):
    if user_question:
        with st.spinner("The AI Agent is analyzing data and generating your report..."):
            try:
                # 1. Create the Agent Executor
                agent_executor = create_agent_executor()
                
                # 2. Invoke the agent with the user's question
                response = agent_executor.invoke({
                    "input": user_question
                })
                
                # 3. Display the final answer
                st.markdown("---")
                st.header("Analysis Report")
                st.markdown(response['output'])
                
            except Exception as e:
                st.error(f"An error occurred: {e}", icon="🚨")
    else:
        st.warning("Please enter a question.", icon="⚠️")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, LangChain, and Ollama.")
