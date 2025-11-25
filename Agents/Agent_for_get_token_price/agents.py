from typing import TypedDict
from classes import State
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
import ForAPi
import requests
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_deepseek import ChatDeepSeek
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from funcs import get_price_tool
from langchain_core.runnables import RunnablePassthrough
from prompts import prompt_for_get_price, prompt_for_router_agent, promt_for_default_llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama
from classes import RouterOutputParser



llm = ChatOllama(
    model='llama3.2:3b'
)
llm2 = ChatMistralAI(
    model_name='mistral-small',
    api_key=ForAPi.api_sec

)
llm3 = ChatMistralAI(
    model_name='mistral-medium',
    api_key=ForAPi.api_sec
)



class OutputR(TypedDict):
    output: str
    next: str
from langchain.agents import create_agent


RoutAgent ={'input': RunnablePassthrough()} | prompt_for_router_agent | llm2.with_structured_output(RouterOutputParser, method='json_schema')
GetPrice_agent =  {'input': RunnablePassthrough() } | prompt_for_get_price | create_agent(model=llm2, tools=[get_price_tool])
AnswerAgent = {'input': RunnablePassthrough()} | promt_for_default_llm | llm | StrOutputParser()



#defautl_llm = {'input': RunnablePassthrough()} | promt_for_default_llm | llm2 | StrOutputParser()


def ROUT_FUNC(state: State):
    response = RoutAgent.invoke(state['input'])
    return {'next_state': response.next_state.value, 'explain': response.explain}





def getPrice(state: State):
    response = GetPrice_agent.invoke(state['output'])
    return {'price' : response['messages'][-1].content, 'next': 'END'}

def get_answer(state: State):
    response = AnswerAgent.invoke(state['input'])
    return {
        'output': response
    }



def call_rout(state: State):
    response = RoutAgent.invoke({f'input': f'{state['input']}'})
    return {'input': state['input'], 'next': response['messages'][-1].content}

def rag_search(state: State):
    pass




# Функция, которая будет активировать RAG поиск по бд.
# Router -> Query Expansion(return {context}) -> RAG SEARCH(return output)