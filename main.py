from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from src.utils.chat import Chat
from src.utils.transactions import Transactions
from src.utils.account import Account
from src.setup import Setup
from parameters import Parameters

Parameters.YEAR = int(input('Año: '))
Parameters.MONTH = int(input('Mes: '))

def main() -> None :
    Setup.main(first_run=Parameters.FIRST_RUN)

    # Get chat dataframe
    chat = Chat(chatPath=Parameters.CHAT_PATH)
    chat_df = chat.get_df()

    # Get transactions dataframe
    transactions = Transactions(chat_df=chat_df, year=Parameters.YEAR, month=Parameters.MONTH)
    transactions_df = transactions.getTransactions()
    
    # Generate the accounts
    Account.TRANSACTIONS = transactions_df
    Account.EXPORT_PATH = Parameters.EXPORT_PATH
    Account.main()
    
    return

main()
