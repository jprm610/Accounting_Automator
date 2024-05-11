from pathlib import Path
from src.chat import Chat
from src.transactions import Transactions
from src.account import Account

CHAT_PATH = Path('Chat de WhatsApp con +57 314 7711497.txt')
EXPORT_PATH = Path('data')
YEAR = int(input('Año: '))
MONTH = int(input('Mes: '))

def main():
    # Get chat dataframe
    chat = Chat(chatPath=CHAT_PATH)
    chat_df = chat.get_df()

    # Get transactions dataframe
    transactions = Transactions(chat_df=chat_df, year=YEAR, month=MONTH)
    transactions_df = transactions.getTransactions()
    
    # Generate the accounts
    Account.TRANSACTIONS = transactions_df
    Account.EXPORT_PATH = EXPORT_PATH
    Account.main()

main()
