import pandas as pd

class Transactions :
    def __init__(self, chat_df: pd.DataFrame, year: int, month: int) -> None:
        self.year = year
        self.month = month
        self.chat_df = chat_df
        self.transactions = self.filterChat(self.chat_df, year=self.year, month=self.month)

    def getTransactions(self) -> pd.DataFrame:
        return self.transactions

    def filterChat(self, chat_df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
        # Convert index to datetime
        chat_df.index = pd.to_datetime(chat_df.index)
        
        # Only transactions that start with an asterisk * and are in the specified year and month
        transactions = chat_df[(chat_df['Message'].str.startswith('*')) & 
                        (chat_df.index.year == year) & 
                        (chat_df.index.month == month)]

        return transactions
