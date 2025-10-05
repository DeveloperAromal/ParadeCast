from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import intiaize_agent,  AgentType,  Tool



def main_agent():

     
    llm = ChatOpenAI(
        model = '',
        base_url = '',
        api_key = ''
    )

