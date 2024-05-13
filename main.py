from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from src.utils.chat import Chat
from src.utils.transactions import Transactions
from src.utils.account import Account
from src.setup import Setup
from parameters import Parameters

def main() -> None :
    print('CONTABILIDAD AUTOMATIZADA')

    print('Configuración inicial...')
    Setup.main(first_run=Parameters.FIRST_RUN)

    print('Elija el año y el mes a generear las cuentas.')
    Parameters.YEAR = int(input('Año (YYYY): '))
    Parameters.MONTH = int(input('Mes (m): '))

    # Get chat dataframe
    print('Cargando chat...')
    chat = Chat(chatPath=Parameters.CHAT_PATH)
    chat_df = chat.get_df()

    # Get transactions dataframe
    print('Generando transacciones...')
    transactions = Transactions(chat_df=chat_df, year=Parameters.YEAR, month=Parameters.MONTH)
    transactions_df = transactions.getTransactions()
    transactions_df.to_csv(Parameters.EXPORT_PATH / 'transactions.csv', index=False)
    
    # Generate the accounts
    print('Generando cuentas...')
    Account.printAccounts()
    generate_more_accounts = input('Agregar más cuentas? (S/N): ')
    if generate_more_accounts in 'sS' :
        new_accounts = input('Nombres de cuentas separados por un espacio: ').split()
        Account.ACCOUNT_NAMES.extend([Transactions.normalize(account) for account in new_accounts])
        Account.printAccounts()       

    Account.TRANSACTIONS = transactions_df
    Account.main()

    print('Proceso finalizado con exito.')
    
    return

main()
