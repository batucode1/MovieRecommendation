from langchain_core.messages import HumanMessage, AIMessage


def run_chatbot(agent):
    chat_history = []

    try:
        user_input = input("\nSiz: ")

        if user_input.lower() in ["çıkış"]:
            print("Sohbet bitti")

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
