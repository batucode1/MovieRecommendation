from langchain_core.tools import tool
from app.vector_store import retriever


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
