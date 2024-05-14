import pandas as pd
from pathlib import Path
from parameters import Parameters

class Account :
    ACCOUNT_NAMES = set()
    TRANSACTIONS = None
    DEBTS_DF = None
    DEBTS = {}
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

        return
    
    def filterTransactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        account_transactions = transactions_df[(transactions_df['ORIGEN'] == self.name) | 
                                               (transactions_df['DESTINO'] == self.name)]
        return account_transactions
    
    def filterAmounts(self, account_transactions: pd.DataFrame) -> pd.DataFrame :
        account_transactions['VALOR'] = account_transactions.apply(lambda x: x['VALOR'] if x['DESTINO'] == self.name else -x['VALOR'], axis=1)
        return account_transactions
    
    def exportAccount(self) -> None :
        if len(self.transactions) > 0 :
            self.transactions.to_csv(Parameters.EXPORT_PATH / f'{self.name} {Parameters.YEAR} {Parameters.MONTH}.csv', index=False)
            print(f'Se exportó {self.name}.')
        
        return

    @classmethod
    def main(cls) -> None :
        for name in Account.ACCOUNT_NAMES : 
            Account(name).exportAccount()

        Account.generateDebtDf(Account.TRANSACTIONS)

        return
    
    @classmethod
    def printAccounts(cls) -> None :
        print('Cuentas a generar:', Account.ACCOUNT_NAMES)
        return
    
    @classmethod
    def generateDebtDf(cls, transactions_df: pd.DataFrame) -> None :
        Account.DEBTS_DF = transactions_df[transactions_df['DEUDOR'] != '.']
        for index, row in Account.DEBTS_DF.iterrows() :
            debt = f"{row['DEUDOR']} -> {row['ORIGEN']}"
            if debt not in Account.DEBTS.keys() :
                Account.DEBTS[debt] = row['VALOR']
            else :
                Account.DEBTS[debt] += row['VALOR']
        settle_debts = pd.DataFrame(Account.DEBTS.items(), columns=['DEUDA', 'VALOR'])
        settle_debts.to_csv(Parameters.EXPORT_PATH / 'Cruce cuentas.csv', index=False)
        Account.DEBTS_DF.to_csv(Parameters.EXPORT_PATH / 'Deudas.csv', index=False)

        print('Se exportó la deuda.')

        return
    
    @classmethod
    def addAccount(cls, new_account:str) -> None :
        if new_account in ['CRUCE', '.'] : return
        Account.ACCOUNT_NAMES.add(new_account)
        return
