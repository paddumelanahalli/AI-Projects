For follow-ups, a simple tool could be "sending an email" (or simulating it).

Create a Python file, e.g., agent_app.py.

Inside agent_app.py, define a function that simulates sending an email:

Python

# agent_app.py
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """Sends an email to a specified recipient with a given subject and body.
    This is a simulated email sending for demonstration purposes.
    """
    print(f"\n--- SIMULATING EMAIL SEND ---")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print(f"---------------------------\n")
    return f"Email to {recipient} with subject '{subject}' simulated successfully."

# You could add other tools, e.g., for looking up calendar events or pulling task data
# @tool
# def get_upcoming_meetings(date: str) -> str:
#     """Retrieves a list of upcoming meetings for a given date."""
#     # In a real scenario, this would integrate with Google Calendar API, Outlook API, etc.
#     return f"No meetings found for {date} (simulated)."
Step 3: Create your Agent

This is where LangChain comes in. You'll use an LLM, your defined tools, and a prompt to guide the agent.

Continue in agent_app.py:

Python

from langchain_openai import ChatOpenAI # or from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_openai_tools_agent # For LangChain's standard agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Initialize your LLM
# If using OpenAI:
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # gpt-4o-mini is cost-effective for testing
# If using Google Gemini:
# llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# Define the tools your agent can use
tools = [send_email] # Add other tools here if you create them

# Define the Agent's Prompt
# This prompt tells the LLM how to act as an agent.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a helpful personal assistant specializing in project management tasks, especially follow-ups.
         Your goal is to help a Senior Director in Engineering Project and Program Management automate repetitive tasks.
         You have access to tools to help with this.
         When asked to send a follow-up, use the 'send_email' tool.
         Be concise and professional in your email content.
         """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the AgentExecutor (the runtime for the agent)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Main interaction loop
if __name__ == "__main__":
    chat_history = []
    print("Personal AI Assistant (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Update chat history for context in future turns
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response["output"]))

        print(f"Agent: {response['output']}")
Step 4: Run your agent!

Save the agent_app.py file.

Run it from your terminal:

Bash

python agent_app.py
Example Interaction:

Personal AI Assistant (Type 'exit' to quit)
You: Can you send a follow-up email to John Doe regarding the action item for the integration demo by Friday?
Agent:
--- SIMULATING EMAIL SEND ---
To: John Doe
Subject: Follow-up: Integration Demo Action Item
Body:
Hi John,

Just a quick follow-up on the action item regarding the integration demo. Please ensure it's completed by Friday.

Thanks,
[Your Name/Agent]
---------------------------
Email to John Doe with subject 'Follow-up: Integration Demo Action Item' simulated succ
