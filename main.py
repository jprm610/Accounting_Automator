from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from src.utils.chat import Chat
from src.utils.transactions import Transactions
from src.utils.account import Account
from src.setup import Setup

FIRST_RUN = False
CHAT_PATH = Path('Chat de WhatsApp con +57 314 7711497.txt')
EXPORT_PATH = Path('data')
YEAR = int(input('Año: '))
MONTH = int(input('Mes: '))

def main() -> None :
    Setup.main(first_run=FIRST_RUN)

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
    
    return

main()
