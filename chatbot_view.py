# ui_streamlit.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from app.create_agent import create_agent  # projenin mevcut ajanı

st.set_page_config(page_title="MovieRAG", page_icon="🎬", layout="centered")

st.title("🎬 MovieRAG")
st.caption("Basit film sohbet asistanı (CSV + Chroma)")

# Ajanı ve geçmişi bir kez oluştur
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
if "history" not in st.session_state:
    st.session_state.history = []  # [("user"/"assistant", text), ...]

# Varsa geçmişi göster
for role, content in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

# Girdi: Enter = gönder (Streamlit'te varsayılan)
prompt = st.chat_input("Bir film sorusu yaz ve Enter'a bas...")

if prompt:
    # Kullanıcı mesajını ekrana ve geçmişe yaz
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # LC geçmişine dönüştür
    lc_history = []
    for role, content in st.session_state.history:
        if role == "user":
            lc_history.append(HumanMessage(content=content))
        else:
            lc_history.append(AIMessage(content=content))

    # Model cevabını akışla yazdır
    full = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            for event in st.session_state.agent.stream({"messages": lc_history}, stream_mode="values"):
                last = event["messages"][-1]
                if isinstance(last, AIMessage):
                    # sadece yeni kısmı ekrana bas
                    delta = last.content[len(full):] if last.content.startswith(full) else last.content
                    full = last.content
                    placeholder.markdown(full)
        except Exception as e:
            full = f"[Hata]: {e}"
            placeholder.markdown(full)

    # Asistan mesajını geçmişe ekle ve sayfayı tazele
    st.session_state.history.append(("assistant", full))
    st.rerun()
