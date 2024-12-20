from pathlib import Path
import pandas as pd
from parameters import Parameters

class Chat :
    def __init__(self, chat_path: Path) -> None :
        """
        @chat_path: Path to the chat file in txt format. \\
        Create a chat object and set the chat dataframe.
        """

        self.chat_df = self.create_df(chat_path=chat_path)

        return

    def create_df(self, chat_path: Path) -> pd.DataFrame:
        """
        @chat_path: Path to the chat file in txt format. \\
        Returns a dataframe with the chat data.
        """

        parsed_data = [] 

        try :
            fp = open(chat_path, 'r', encoding="utf-8")
        except :
            raise FileNotFoundError('No hay chats en la ruta del archivo.')
        
        lines = fp.readlines()
        
        message_buffer = []
        for line in lines :
            line = line.replace('\u202f', ' ')
            line = line.replace('p. m.', 'PM').replace('a. m.', 'AM')
            line = line.strip()
            if Chat.Start_With_Date_And_Time(line) : 
                if len(message_buffer) > 0 : 
                    parsed_data.append([date_time, author, ' '.join(message_buffer)]) 
                message_buffer.clear() 
                date_time, author, message = Chat.Get_Data_Point(line)
                message_buffer.append(message)
            else:
                message_buffer.append(line)

        fp.close()

        chat = pd.DataFrame(parsed_data, columns=['Date_Time', 'Author', 'Message'])

        chat["Date_Time"] = pd.to_datetime(chat["Date_Time"], dayfirst=True)
        chat['date'] = [d.date() for d in chat['Date_Time']]
        del chat['Date_Time']

        chat.set_index('date', inplace=True)

        chat = pd.DataFrame(parsed_data, columns=['Date_Time', 'Author', 'Message'])

        chat["Date_Time"] = pd.to_datetime(chat["Date_Time"], dayfirst=True)
        chat['date'] = [d.date() for d in chat['Date_Time']]
        del chat['Date_Time']

        chat.set_index('date', inplace=True)

        return chat
    
    def getChat_df(self) -> pd.DataFrame:
        """
        Returns the chat dataframe.
        """

        return self.chat_df
    
    @classmethod
    def Start_With_Date_And_Time(cls, s) -> bool :
        """
        @s: String to check if it starts with a date and time. \\
        Returns True if the string starts with a date and time, False otherwise.
        """

        import re

        if Parameters.LANGUAGE == 'ES' :
            pattern = "^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}\S [AaPp][Mm] -"
        elif Parameters.LANGUAGE == 'FR' :
            pattern = "^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2} -"

        result = re.match(pattern, s)

        return bool(result)
    
    @classmethod
    def Get_Data_Point(cls, line) -> tuple :
        """
        @line: Line of the chat. \\
        Returns a tuple with the date and time, author and message.
        """

        split_line = line.split(' - ') 
        date_time = split_line[0]
        message = ' '.join(split_line[1:])
        if Chat.Find_Author(message): 
            split_message = message.split(': ') 
            author = split_message[0] 
            message = ' '.join(split_message[1:])
        else:
            author = None
        return date_time, author, message

    @classmethod
    def Find_Author(cls, s) -> bool:
        """
        @s: String to check if it contains an author.
        Returns True if the string contains an author, False otherwise.
        """

        import re

        # Patterns to match different author name formats
        patterns = [
            "([\w]+):",                      # First name only
            "([\w]+[\s]+[\w]+):",            # First name + Last name
            "([\w]+[\s]+[\w]+[\s]+[\w]+):",  # First name + Middle name + Last name
            "([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):" # First name + Middle name + Last name + Suffix
        ]

        # Combine the patterns into one
        pattern = '^' + '|'.join(patterns)

        # Check if the string matches any of the patterns
        result = re.match(pattern, s)
        #result = re.match(pattern, s.strip().split('-')[1].strip() if '-' in s else s)

        return bool(result)

    """
    @classmethod
    def Find_Author(cls, s) -> bool :
        
        @s: String to check if it contains an author. \\
        Returns True if the string contains an author, False otherwise.
        

        import re

        patterns = [
            "([\w]+):",                     # Nombre
            "([\w]+[\s]+[\w]+):",           # Nombre + Apellido
            "([\w]+[\s]+[\w]+[\s]+[\w]+):", # Nombre + Segundo Nombre + Apellido
        ]

        pattern = '^' + '|'.join(patterns)

        result = re.match(pattern, s)
    """
