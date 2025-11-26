from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
import langchain
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache # Use this for modern LangChain

# Import the tools we created
from tools import query_sales_data, get_inventory_levels, generate_demand_forecast

def create_agent_executor():
    """
    Creates and returns the LangChain agent executor.
    """
    # --- 1. Set up Caching ---
    set_llm_cache(InMemoryCache())

    # --- 2. Initialize the LLM ---
    # Use mistral as requested
    llm = Ollama(model="mistral", temperature=0)

    # --- 3. Define the tools ---
    tools = [query_sales_data, get_inventory_levels, generate_demand_forecast]

    # --- 4. Create the Prompt Template ---
    # This is the core logic of the agent. It tells the LLM how to reason and act.
    prompt_template = """
    You are a helpful Retail Analyst AI Agent. Your goal is to provide demand forecasts and inventory recommendations.

    Answer the user's question as best as possible. You have access to the following tools:

    {tools}

    To use a tool, please use the following format:

    Thought: Do I need to use a tool? Yes
    Action: The action to take, should be one of [{tool_names}]
    Action Input: The input to the action (must be a single dictionary object matching the tool's schema)
    Observation: The result of the action

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

    Thought: Do I need to use a tool? No
    Final Answer: [Your comprehensive response here]

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)


    # --- 5. Create the Agent ---
    # The ReAct (Reasoning and Acting) agent is a good general-purpose choice.
    agent = create_react_agent(llm, tools, prompt)

    # --- 6. Create the Agent Executor ---
    # The executor is what runs the agent and its tools.
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, # Set to True to see the agent's thought process
        handle_parsing_errors=True # Gracefully handle any LLM output parsing errors
    )

    return agent_executor

if __name__ == '__main__':
    # This is for testing the agent directly from the command line
    agent_executor = create_agent_executor()
    
    print("Retail AI Agent is ready. Ask a question.")
    
    # Example question
    question = "What is the demand forecast for Product A for the next 30 days, and should we reorder?"
    print(f"Question: {question}")
    
    response = agent_executor.invoke({
        "input": question
    })
    
    print("\n--- Final Response ---")
    print(response['output'])