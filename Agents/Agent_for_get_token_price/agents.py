
from typing import TypedDict

from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
import ForAPi
import requests
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from funcs import get_price_of_token, get_price_tool
from langchain_core.runnables import RunnablePassthrough
from prompts import prompt_for_get_price, prompt_for_router_agent
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama

llm2 = ChatOllama(
    model='llama3.2:3b'
)

llm = ChatMistralAI(
    model_name='mistral-small',
    api_key=ForAPi.api_sec

)
class OutputR(TypedDict):
    output: str
    next: str

from langchain.agents import create_agent


RoutAgent ={'input': RunnablePassthrough()} | prompt_for_router_agent | create_agent(model=llm2, tools=[])
GetPrice_agent =  {'input': RunnablePassthrough() } | prompt_for_get_price | create_agent(model=llm2, tools=[get_price_tool])


class State(TypedDict):
    input: str
    next: str
    price: str
    output: str


def ROUT_FUNC(state: State):
    response = RoutAgent.invoke(state['input'])
    return {'output': state['input'], 'next': response['messages'][-1].content}





def getPrice(state: State):
    response = GetPrice_agent.invoke(state['output'])
    return {'price' : response['messages'][-1].content, 'next': 'END'}





def call_rout(state: State):
    response = RoutAgent.invoke({f'input': f'{state['input']}'})
    return {'input': state['input'], 'next': response['messages'][-1].content}




