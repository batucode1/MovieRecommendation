from app.run_chat import run_chatbot
from app.create_agent import create_agent

while True:
    agent=create_agent()
    run_chatbot(agent)