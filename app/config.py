import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_DISABLED"] = "true"
load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
movies_file = "data/movies.csv"

# verileri sayısal verilere dönüştürecek huggingface modeli hazırlandı
embedding_model = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
embedding = HuggingFaceEmbeddings(
    model_name=embedding_model)

# denemek için daha küçük model -> sentence-transformers/all-MiniLM-L6-v2