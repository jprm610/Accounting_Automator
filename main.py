from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from src.utils.chat import Chat
from src.utils.transactions import Transactions
from src.utils.account import Account
from src.utils.debt import Debt
from src.setup import Setup
from parameters import Parameters

def main() -> None :
    print('CONTABILIDAD AUTOMATIZADA')

    print('Configuración inicial...')
    Setup.main(first_run=Parameters.FIRST_RUN)

    print('Elija el año y el mes para generar las cuentas.')
    Parameters.YEAR = int(input('Año (YYYY): '))
    Parameters.MONTH = int(input('Mes (m): '))

    # Get chat dataframe
    print('Cargando chat...')
    chat = Chat(chat_path=Parameters.INPUT_PATH)
    chat_df = chat.getChat_df()

    # Get transactions dataframe
    print('Generando transacciones...')
    transactions = Transactions(chat_df=chat_df, year=Parameters.YEAR, month=Parameters.MONTH)
    transactions_df = transactions.getTransactions()
    transactions_df.to_csv(Parameters.EXPORT_PATH / 'transactions.csv', index=False)
    
    # Generate the accounts
    print('Generando cuentas...')
    Account.printAccounts() 
    Account.GLOBAL_TRANSACTIONS = transactions_df
    Account.main()

    # Generate the debts
    print('Generando deudas...')
    Debt.generateDebtsDf(Account.GLOBAL_TRANSACTIONS)
    Debt.main()

    print('Proceso finalizado con exito.')
    
    return

main()
