class Transaction :
    def __init__(self, date, message:str) -> None :
        self.date = date
        self.sender = None
        self.recipient = None
        self.debt = None
        self.description = None
        self.amount = None
        self.messageToTransaction(message)

        return

    def messageToTransaction(self, message:str) -> None :
        import re

        message = message.split(' ')
        self.sender = message[0]
        self.recipient = message[1]
        self.debt = '.'
        start_index_description = 2
        match = re.search(r'\((\w+)\)', message[2])
        if match:
            self.debt = match.group(1)
            start_index_description = 3
        self.description = ' '.join(message[start_index_description:])
        self.amount = Transaction.getAmount(self.description)

        return

    def getTransaction(self) -> dict :
        return {
            'FECHA': self.date,
            'ORIGEN': self.sender,
            'DESTINO': self.recipient,
            'LE DEBE': self.debt,
            'DESCRIPCION': self.description,
            'VALOR': self.amount
        }

    @classmethod
    def getAmount(cls, description:str) -> int :
        return sum([int(x) for x in description.split() if x.isnumeric()])
