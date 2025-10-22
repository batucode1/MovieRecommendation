from langgraph.prebuilt import create_react_agent
from .config import model
from .tools import retrieve_movie_context

SYSTEM_PROMPT = (
    "Sen filmler hakkında bilgi veren yardımcı bir asistansın. "
    "Kullanıcının sorularını yanıtlamak için 'retrieve_movie_context' aracını kullanmalısın. "
    "Bu aracı kullanarak film veritabanından bilgi çekersin."
    "Sana verilen bağlam (context) dışındaki bilgilere dayanarak cevap verme."
    "Eğer araçtan gelen bilgide cevap yoksa, 'Üzgünüm, bu bilgi veritabanımda bulunmuyor.' de."
    "Cevaplarını her zaman Türkçe ver."
)

def create_agent():
    tool = [retrieve_movie_context]
    agent = create_react_agent(model, tool, prompt=SYSTEM_PROMPT)
    return agent