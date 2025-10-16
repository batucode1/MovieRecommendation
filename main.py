import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
store = {}
movies = "data/movies.csv"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a film reviewer. Answer all questions with make use of the documents"),
        MessagesPlaceholder(variable_name="messages")
    ]
)
try:
    df = pd.read_csv(movies)
    print("başarılı")
    print(df.columns)
except FileNotFoundError:
    print("hata")
