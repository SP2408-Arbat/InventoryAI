# Retail AI Agent

This project implements an AI agent that provides demand forecasts and inventory recommendations for retail managers.

## Setup

1.  **Install Ollama:** Make sure you have Ollama installed and running. You can download it from [https://ollama.ai/](https://ollama.ai/).

2.  **Pull a model:** Pull a model for the agent to use. We recommend `mistral` or `llama3`.
    ```bash
    ollama pull mistral
    ```

3.  **Install Dependencies:** Create a virtual environment and install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Generate Data:** Run the data generator to create synthetic sales and inventory data.
    ```bash
    python data_generator.py
    ```

2.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

3.  Open your browser to the local URL provided by Streamlit to interact with the agent.
