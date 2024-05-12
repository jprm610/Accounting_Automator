import pandas as pd
from src.utils.transaction import Transaction

class Transactions :
    def __init__(self, chat_df: pd.DataFrame, year: int, month: int) -> None :
        self.year = year
        self.month = month
        self.chat_df = chat_df
        self.chat_df = self.filterChat(chat_df=self.chat_df, year=self.year, month=self.month)
        self.transactions = self.convertToTransactionsFormat(chat_df=self.chat_df)

        return

    def getTransactions(self) -> pd.DataFrame:
        return self.transactions

    def filterChat(self, chat_df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
        # Convert index to datetime
        chat_df.index = pd.to_datetime(chat_df.index)
        
        # Only transactions that start with an asterisk * and are in the specified year and month
        chat_df = chat_df[(chat_df['Message'].str.startswith('*')) & 
                        (chat_df.index.year == year) & 
                        (chat_df.index.month == month)]

        chat_df['Message'] = chat_df['Message'].apply(Transactions.normalize)

        return chat_df
    
    def convertToTransactionsFormat(self, chat_df: pd.DataFrame) -> pd.DataFrame:
        transactions = [Transaction(date, message).getTransaction() for date, message in zip(chat_df.index, chat_df['Message'])]
        transactions = pd.DataFrame(transactions)
        #transactions.set_index('date', inplace=True)
        return transactions
    
    @classmethod
    def normalize(cls, s:str) -> str :
        replacements = (
            ('*', ''),
            ("Á", "A"),
            ("É", "E"),
            ("Í", "I"),
            ("Ó", "O"),
            ("Ú", "U"),
        )
        s = s.strip()
        s = s.upper()
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        s = s.replace("<SE EDITO ESTE MENSAJE.>", '')

        return s
