from typing import TypedDict, Literal
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from agents import RoutAgent, GetPrice_agent, ROUT_FUNC, getPrice
from agents import State
from IPython.display import display, Image
from PIL import Image as PILImage
import io





graph = StateGraph(State)


graph.add_node('router', ROUT_FUNC)
graph.add_node('price', getPrice)
#graph.set_entry_point('price')
graph.set_entry_point('router')

graph.add_edge('router','price')
#graph.set_finish_point('price')
graph.add_edge('price', END)
itg = graph.compile()

resp = itg.invoke({'input': 'Сколько стоит тонкоин?'})


print(resp)



