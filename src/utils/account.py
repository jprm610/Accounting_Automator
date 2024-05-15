import pandas as pd
from pathlib import Path
from parameters import Parameters
from src.utils.debt import Debt

class Account :
    ACCOUNT_NAMES = set()
    GLOBAL_TRANSACTIONS = None
    def __init__(self, name:str) -> None:
        """
        @name: Account name.
        Creates an account object with the name and sets the account's transactions.
        """
        self.name = name
        self.transactions = None
        # Set account's transactions
        self.setAccount()
        return

    def getTransactions(self) -> pd.DataFrame:
        """
        Get transactions for the account.
        """
        return self.transactions
    
    def setTransactions(self, transactions: pd.DataFrame) -> None :
        """
        Set transactions for the account.
        """
        self.transactions = transactions
        return
    
    def filterTransactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame :
        """
        @transactions_df: DataFrame with all transactions. \\
        Returns transactions related to the account.
        """

        # Get transcations where the account is the origin or destination
        account_transactions = transactions_df[(transactions_df['ORIGEN'] == self.name) | 
                                               (transactions_df['DESTINO'] == self.name)]
        return account_transactions
    
    def filterAmounts(self, account_transactions: pd.DataFrame) -> pd.DataFrame :
        """
        @account_transactions: DataFrame with transactions related to the account. \\
        Returns transactions with the amount deposited or withdrawn.
        """

        # Define if the amount was deposited or withdrawn whether the account is the origin or destination
        account_transactions['VALOR'] = account_transactions.apply(lambda x: x['VALOR'] if x['DESTINO'] == self.name else -x['VALOR'], axis=1)
        return account_transactions
    
    def setAccount(self) -> None :
        """
        Filter transactions for the account and set the account's transactions.
        Defining if the amount was deposited or withdrawn.
        """

        # Filter transactions for the account
        self.setTransactions(self.filterTransactions(Account.GLOBAL_TRANSACTIONS))

        # Define if the amount was deposited or withdrawn
        self.setTransactions(self.filterAmounts(self.getTransactions()))

        return
    
    def exportAccount(self) -> None :
        """
        Export the account's transactions to a csv file.
        """

        # Export the account's transactions if there are transactions
        if len(self.getTransactions()) > 0 :
            self.getTransactions().to_csv(Parameters.EXPORT_PATH / f'{self.name} {Parameters.YEAR} {Parameters.MONTH}.csv', index=False)
            print(f'Se exportó {self.name}.')
        
        return

    @classmethod
    def main(cls) -> None :
        """
        Generate the accounts to generate and export the transactions for each account.
        """

        for name in Account.ACCOUNT_NAMES : 
            Account(name).exportAccount()

        return
    
    @classmethod
    def printAccounts(cls) -> None :
        """
        Print the accounts to generate.
        """

        print('Cuentas a generar:', Account.ACCOUNT_NAMES)
        return
    
    @classmethod
    def addAccount(cls, new_account:str) -> None :
        """
        @new_account: New account to add to the accounts to generate. \\
        Add the new account to the accounts to generate dinamically.
        """

        # Check if the account is not 'CRUCE' or '.' and add it to the accounts to generate.
        if new_account in ['CRUCE', '.'] : return
        Account.ACCOUNT_NAMES.add(new_account)
        return
