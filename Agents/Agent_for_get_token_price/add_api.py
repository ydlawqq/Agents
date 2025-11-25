from contextlib import asynccontextmanager
from main_graph import graph
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from langgraph.checkpoint.memory import InMemorySaver, MemorySaver
l ={}

@asynccontextmanager
async def lifespan(app: FastAPI):
    memory = MemorySaver()
    memory_store = InMemorySaver
    l['getStart'] = graph.compile(checkpointer=memory, store=memory_store)
    yield
    l.clear()

app = FastAPI(title='Agent API', lifespan=lifespan)

from langgraph.checkpoint.sqlite import SqliteSaver

# Query Schema for requests
class QueryRequest(BaseModel):
    checkpoint_id: str
    input: str


@app.get('/')
def read_root():
    return {'Hello': 'World'}




@app.post('/invoke')
def invoke(query: QueryRequest):
    config = {'configurable': {'checkpoint_id': query.checkpoint_id, 'thread_id': query.checkpoint_id}}
    response = l['getStart'].invoke({'input': query.input}, config=config)
    return {
        'response': response.get('output'),
        'thread_id': query.checkpoint_id
    }



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000 )