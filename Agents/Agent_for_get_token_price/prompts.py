from langchain_core.prompts import ChatPromptTemplate
prompt_for_get_price = ChatPromptTemplate([
    ('system', "Ты — крипто-агент. Твоя задача — получить актуальную цену токена.\n"
    "Используй инструменты, когда нужно получить данные.\n"
    "Никогда не выдумывай цену — только если инструмент дал ответ.\n"
    "Отвечай кратко и точно."

     ),
    ('user', '{input}')
])



prompt_for_router_agent = ChatPromptTemplate([('system', """
Ты — роутер для LLM-агента. Решай, что делать дальше.

Доступные действия:
- answer: если можешь ответить напрямую (факты, общие знания, логика)
- price: если хочешь узнать цену токена в данный момент

Верни ТОЛЬКО JSON в формате:
{{"next_state": *следующее выбранное действи*, "reasoning": *объяснение, почему выбрал именно его*}}

"""),
                                              ('user', '{input}')])


config= {'configurable': {'thread_id': 'user_test'}}


promt_for_default_llm = ChatPromptTemplate([
    ('system', 'Ты - помощник, отвечай на вопросы пользователя, поддерживай хорошее настроение'),
    ('user', '{input}')


])