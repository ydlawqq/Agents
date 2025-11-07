from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI
import glob
from langchain_mistralai.chat_models import SecretStr
from langchain_mistralai.embeddings import MistralAIEmbeddings

api = 'WdIZEvLAwsmM3cefzH2Q6wAPTCI9a0xF'
docs = []
for path in glob.glob('/home/ydlawq/Загрузки/OOP_lektsii-1.pdf'):
    loader = PyPDFLoader(path)
    docs.extend(loader.load())

llm = ChatMistralAI(
    api_key=api,
    model_name='mistral-medium'
)

embeds = MistralAIEmbeddings(
    model='mistral-embed',
    api_key=api
)



splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=5,
    length_function=lambda x: len(x.split('.')),
    is_separator_regex=False
)

chunks = splitter.split_documents(docs)

vectordatabase = Chroma.from_documents(
    embedding=embeds,
    documents=chunks
)

retriever = vectordatabase.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 5}
)






prompt = ChatPromptTemplate([
    ('system', 'Ты помощник студента, который изучил все лекции, ответь ему строго по прелоставленному текста, не добавляя ничего своего и не изменяя никакие термины. Текст: "{context}"'),
    ('user', '{query}')
])
rag_chain = ({'context': retriever, 'query': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser())



answer = rag_chain.invoke('Какие бывают модификаторы доступа?')


print(answer)
