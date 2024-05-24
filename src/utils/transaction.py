from src.utils.account import Account

class Transaction :
    def __init__(self, date, message:str) -> None :
        """
        @date: Date of the transaction. \\
        @message: Whatsapp message with the transaction. \\
        Creates a transaction object with the date and message,
        and sets the transaction attributes.
        """

        self.date = date
        self.sender = None
        self.recipient = None
        self.debtor = None
        self.description = None
        self.amount = None
        self.messageToTransaction(message)

        return

    def messageToTransaction(self, message:str) -> None :
        """
        @message: Whatsapp message with the transaction. \\
        Set the transaction attributes from the message.
        """

        import re

        # Split the message
        message = message.split(' ')
        self.sender = message[0]
        self.recipient = message[1]
        self.debtor = '.'
        start_index_description = 2
        # Check if the message has a debtor
        match = re.search(r'\((\w+)\)', message[2])
        if match:
            # Set the debtor
            self.debtor = match.group(1)
            start_index_description = 3
        self.description = ' '.join(message[start_index_description:])
        self.amount = Transaction.getAmount(self.description)

        # Add accounts dinamically
        Account.addAccount(self.sender)
        Account.addAccount(self.recipient)
        Account.addAccount(self.debtor)

        return

    def getTransaction(self) -> dict :
        # Return the transaction as a dictionary

        return {
            'FECHA': self.date,
            'ORIGEN': self.sender,
            'DESTINO': self.recipient,
            'DEUDOR': self.debtor,
            'DESCRIPCION': self.description,
            'VALOR': self.amount
        }

    @classmethod
    def getAmount(cls, description:str) -> int :
        """
        @description: Description of the transaction. \\
        Returns the amount of the transaction.
        """

        # Return the sum of the numbers in the description
        return sum([int(x) for x in description.split() if x.isnumeric() and int(x) >= 1000])
