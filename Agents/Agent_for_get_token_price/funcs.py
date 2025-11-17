from pysendpulse.pysendpulse import PySendPulse
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
import requests
from ForAPi import api_sec, api_id, api_secret
from langchain_core.tools import tool

MEMCACHED_HOST = '127.0.0.1:11211'
llm = ChatMistralAI(
    model_name='mistal-medium',
    api_key=api_sec
)
key = api_id
BASE_URL = "https://api.unisender.com/ru/api/sendEmail"

class TokenPriceInput(BaseModel):
    token_name: str = Field(description="Тикер токена, например BTC, ETH, NOT")


def get_price_of_token(token_name: str):
    'Получает цену токена на Бинанс'
    return requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={token_name.upper()}USDT').json()['price']

get_price_tool = StructuredTool.from_function(
    func=get_price_of_token,
    name="get_price_of_token",
    description="Получает текущую цену токена на Binance. Пример: 'BTC', 'ETH', 'NOT'",
    args_schema=TokenPriceInput
)

