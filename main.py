from src.chat import Chat

CHAT_PATH = 'Chat de WhatsApp con +57 314 7711497.txt'

def main():
    # Get chat dataframe
    chat = Chat(chatPath=CHAT_PATH)
    chat_df = chat.get_df()
    print(chat_df)
    
main()
