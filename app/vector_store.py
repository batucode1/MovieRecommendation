import pandas as pd
from langchain_community.vectorstores import Chroma
from .config import movies_file, embedding
from langchain_huggingface import HuggingFaceEmbeddings


# chunk işlemi
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


moviesDf = pd.read_csv(movies_file)

# chunking

# döküman oluşturuluyor
document = moviesDf.apply(createFilmDocument, axis=1).tolist()
# veriler ve sayısal karşılıkları vectorstorea kaydedildi chrome vectordb ile
vectorstore = Chroma.from_texts(
    texts=document,
    embedding=embedding,
)
retriever = vectorstore.as_retriever()
