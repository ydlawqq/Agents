from typing import TypedDict, Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from agents import RoutAgent, GetPrice_agent, ROUT_FUNC, getPrice, get_answer
from agents import State
from funcs import next_node
from langgraph.checkpoint.sqlite import SqliteSaver


from IPython.display import display, Image
from PIL import Image as PILImage
import io
from dotenv import load_dotenv

load_dotenv()
from prompts import config


graph = StateGraph(State)


graph.add_node('router', ROUT_FUNC)
graph.add_node('price', getPrice)
graph.add_node('answer', get_answer)
graph.set_entry_point('router')

graph.add_conditional_edges('router',lambda x: x['next_state'], {'price': 'price', 'answer': 'answer'})

graph.add_edge('price', END )

graph.set_finish_point('answer')

