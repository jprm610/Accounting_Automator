import pandas as pd
from pathlib import Path

class Account :
    ACCOUNT_NAMES = ['R2', 'ROS', 'VAL', 'R2GRV', 'GRV', 'EF']
    EXPORT_PATH = Path('data')
    TRANSACTIONS = None
    def __init__(self, name:str) -> None:
        self.name = name
        self.setAccount(Account.TRANSACTIONS)

    def getTransactions(self) -> pd.DataFrame:
        return self.transactions

    def setAccount(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        self.transactions = self.filterTransactions(transactions_df)
        self.transactions = self.filterAmounts(self.transactions)
    
    def filterTransactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        account_transactions = transactions_df[(transactions_df['sender'] == self.name) | 
                                               (transactions_df['recipient'] == self.name)]
                                               
        return account_transactions
    
    def filterAmounts(self, account_transactions: pd.DataFrame) -> pd.DataFrame :
        account_transactions['amount'] = account_transactions.apply(lambda x: x['amount'] if x['recipient'] == self.name else -x['amount'], axis=1)
        return account_transactions
    
    def exportAccount(self) :
        self.transactions.to_csv(Account.EXPORT_PATH / f'{self.name}.csv', index=False)
    
    @classmethod
    def main(cls) :
        for name in Account.ACCOUNT_NAMES : 
            Account(name).exportAccount()
            print(f'Se exportó {name}.')
