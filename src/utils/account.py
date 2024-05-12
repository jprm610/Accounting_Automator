import pandas as pd
from pathlib import Path
from parameters import Parameters

class Account :
    ACCOUNT_NAMES = ['R2', 'ROS', 'VAL', 'R2GRV', 'GRV', 'EF', 'OLG', 'R2CG']
    TRANSACTIONS = None
    def __init__(self, name:str) -> None:
        self.name = name
        self.transactions = None
        self.debt = None
        self.setAccount()
        return

    def getTransactions(self) -> pd.DataFrame:
        return self.transactions

    def setAccount(self) -> None :
        self.transactions = self.filterTransactions(Account.TRANSACTIONS)
        self.transactions = self.filterAmounts(self.transactions)

        self.debt = self.filterDebt(Account.TRANSACTIONS)
        return
    
    def filterTransactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        account_transactions = transactions_df[(transactions_df['sender'] == self.name) | 
                                               (transactions_df['recipient'] == self.name)]
        return account_transactions
    
    def filterAmounts(self, account_transactions: pd.DataFrame) -> pd.DataFrame :
        account_transactions['amount'] = account_transactions.apply(lambda x: x['amount'] if x['recipient'] == self.name else -x['amount'], axis=1)
        return account_transactions
    
    def filterDebt(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        debt = transactions_df[transactions_df['debt'] == self.name]
        return debt
    
    def exportAccount(self) -> None :
        if len(self.transactions) > 0 :
            print(f'Se exportó {self.name}.')
            self.transactions.to_csv(Parameters.EXPORT_PATH / f'{self.name} {Parameters.YEAR} {Parameters.MONTH}.csv', index=False)

        if len(self.debt) > 0 :
            print(f'Se exportó {self.name} (Deudas).')
            self.debt.to_csv(Parameters.EXPORT_PATH / f'{self.name} {Parameters.YEAR} {Parameters.MONTH} Deudas.csv', index=False)
        return
    
    @classmethod
    def main(cls) -> None :
        for name in Account.ACCOUNT_NAMES : 
            Account(name).exportAccount()
        return
