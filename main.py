import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from config import movies_file, embedding

#os.environ["TOKENIZERS_PARALLELISM"] = "false"
#os.environ["ANONYMIZED_TELEMETRY"] = "False"
#os.environ["CHROMA_TELEMETRY_DISABLED"] = "true"

#load_dotenv()

#model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

#movies_file = "data/movies.csv"

moviesDf = pd.read_csv(movies_file)


# chunking
def createFilmDocument(row):
    title = row.get("title", "N/A")
    genre = row.get("genre", "N/A")
    director = row.get("director", "N/A")
    actors_1 = row.get("actors_1", "N/A")
    actors_2 = row.get("actors_2", "N/A")
    description = row.get("description", "N/A")
    actors_string = f"{actors_1}, {actors_2}".strip(", ")
    year = row.get("year", "N/A")
    duration = row.get("duration", "N/A")
    country = row.get("country", "N/A")
    language = row.get("language", "N/A")
    writer = row.get("writer", "N/A")
    desc35 = row.get("desc35", "N/A")
    avg_imdb = row.get("avg_imdb", "N/A")
    budget = row.get("budget", "N/A")
    worldwide_gross_income = row.get("worldwide_gross_income", "N/A")

    if actors_string == "N/A, N/A" or not actors_string:
        actors_string = "Belirtilmemiş"
    return f"""Film Adı: {title}
Türü: {genre}
Yönetmen: {director}
Başrol Oyuncuları: {actors_string}
Konu Özeti: {description}
Çekim Yılı: {year}
Film Süresi:{duration}
Bölge:{country}
Dil: {language}
Yazar:{writer}
Başlık:{desc35}
Ortalama IMDB:{avg_imdb}
Bütçe:{budget}
Dünya Geneli İnceleme:{worldwide_gross_income}
"""


# döküman oluşturuluyor
document = moviesDf.apply(createFilmDocument, axis=1).tolist()

# verileri sayısal verilere dönüştürecek huggingface modeli hazırlandı
embedding_model = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
embedding = HuggingFaceEmbeddings(model_name=embedding_model)

# veriler ve sayısal karşılıkları vectorstorea kaydedildi chrome vectordb ile
vectorstore = Chroma.from_texts(
    texts=document,
    embedding=embedding,
)

# retrieve vectordbden yani chromadan sonuçları getirmeye yarar
retriever = vectorstore.as_retriever()


@tool
def retrieve_movie_context(query: str) -> str:
    """
    Kullanıcının film sorgusunu yanıtlamak için film veritabanından
    ilgili film bilgilerini (konu, tür, oyuncular) getir.
    """
    retrieve_docs = retriever.invoke(query)

    serialized = "\n---\n".join(
        doc.page_content for doc in retrieve_docs
    )
    return serialized


tools = [retrieve_movie_context]

SYSTEM_PROMPT = (
    "Sen filmler hakkında bilgi veren yardımcı bir asistansın. "
    "Kullanıcının sorularını yanıtlamak için 'retrieve_movie_context' aracını kullanmalısın. "
    "Bu aracı kullanarak film veritabanından bilgi çekersin."
    "Sana verilen bağlam (context) dışındaki bilgilere dayanarak cevap verme."
    "Eğer araçtan gelen bilgide cevap yoksa, 'Üzgünüm, bu bilgi veritabanımda bulunmuyor.' de."
    "Cevaplarını her zaman Türkçe ver."
)

agent = create_react_agent(model, tools, prompt=SYSTEM_PROMPT)
print("Çıkmak için 'çıkış' yazın.")

# sohbet geçmişi tutulur listede
chat_history = []

while True:
    try:
        user_input = input("\nSiz: ")

        if user_input.lower() in ["çıkış"]:
            print("Sohbet bitti")
            break

        # kullanıcının mesajını ekler
        chat_history.append(HumanMessage(content=user_input))
        print("...\n")

        # agent çalışırken sohbet geçmişini alır
        # çok konuşmak sohbet geçmişini uzatır yavaslar
        events = agent.stream(
            {"messages": chat_history},
            stream_mode="values"
        )

        full_response = ""

        for event in events:
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage):
                if last_message.content == full_response:
                    continue

                print(f"{last_message.content[len(full_response):]}", end="", flush=True)
                full_response = last_message.content
        if full_response:
            chat_history.append(AIMessage(content=full_response))

    except Exception as e:
        print(e)
