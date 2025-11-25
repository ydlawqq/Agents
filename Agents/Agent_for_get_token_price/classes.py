from typing import TypedDict
from pydantic import BaseModel, Field
from enum import Enum



# State schema for graph states, may be not full
class State(TypedDict):
    input: str
    next: str
    price: str
    output: str

# Schema for tool input
class TokenPriceInput(BaseModel):
    token_name: str = Field(description="Тикер токена, например BTC, ETH, NOT")


class OutputR(TypedDict):
    output: str
    next: str

class PossibleStates(str, Enum):
    ANSWER = "answer"
    PRICE = 'price'

class RouterOutputParser(BaseModel):
    next_state: PossibleStates = Field(description='Название следующего узла')
    explain: str = Field(description='Объяснение, почему ты выбрал именно его ')