import pandas as pd
from src.utils.transaction import Transaction

class Transactions :
    def __init__(self, chat_df: pd.DataFrame, year: int, month: int) -> None :
        """
        @chat_df: Chat dataframe. \\
        @year: Year to filter the transactions. \\
        @month: Month to filter the transactions. \\
        Create a transactions object and set the transactions dataframe.
        """

        self.year = year
        self.month = month
        self.chat_df = chat_df
        self.chat_df = self.filterChat(chat_df=self.chat_df, year=self.year, month=self.month)
        self.transactions = self.convertToTransactionsFormat(chat_df=self.chat_df)

        return

    def getTransactions(self) -> pd.DataFrame:
        """
        Returns the transactions dataframe.
        """

        return self.transactions

    def filterChat(self, chat_df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
        """
        @chat_df: Chat dataframe. \\
        @year: Year to filter the transactions. \\
        @month: Month to filter the transactions. \\
        Returns the chat dataframe with the transactions filtered by year and month.
        """

        # Convert index to datetime
        chat_df.index = pd.to_datetime(chat_df.index)
        
        # Only transactions that start with an asterisk * and are in the specified year and month
        chat_df = chat_df[(chat_df['Message'].str.startswith('*')) & 
                        (chat_df.index.year == year) & 
                        (chat_df.index.month == month)]

        chat_df['Message'] = chat_df['Message'].apply(Transactions.normalize)

        return chat_df
    
    def convertToTransactionsFormat(self, chat_df: pd.DataFrame) -> pd.DataFrame:
        """
        @chat_df: Chat dataframe. \\
        Returns the transactions dataframe in transactions format.
        """

        transactions = [Transaction(date, message).getTransaction() for date, message in zip(chat_df.index, chat_df['Message'])]
        transactions = pd.DataFrame(transactions)
        #transactions.set_index('date', inplace=True)
        return transactions
    
    @classmethod
    def normalize(cls, s:str) -> str :
        """
        @s: String to normalize. \\
        Returns the normalized string.
        """

        replacements = (
            ('*', ''),
            ("Á", "A"),
            ("É", "E"),
            ("Í", "I"),
            ("Ó", "O"),
            ("Ú", "U"),
        )
        s = s.upper()
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        s = s.replace("<SE EDITO ESTE MENSAJE.>", '')
        s = s.strip()

        return s
