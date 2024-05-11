from pathlib import Path
import pandas as pd

class Chat :
    def __init__(self, chatPath: Path) -> None:
        self.chatPath = chatPath
        self.df = self.create_df(self.chatPath)

    def create_df(self, chatPath: Path) -> pd.DataFrame:
        parsed_data = [] 

        fp = open(chatPath, 'r', encoding="utf-8")
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
    
    def get_df(self) -> pd.DataFrame:
        return self.df
    
    @classmethod
    def Start_With_Date_And_Time(cls, s) :
        import re

        pattern = "^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}\S [AaPp][Mm] -"
        result = re.match(pattern, s)

        if result :
            return True

        return False
    
    @classmethod
    def Get_Data_Point(cls, line) :
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
    def Find_Author(cls, s) :
        import re

        patterns = [
            "([\w]+):",                     # Nombre
            "([\w]+[\s]+[\w]+):",           # Nombre + Apellido
            "([\w]+[\s]+[\w]+[\s]+[\w]+):", # Nombre + Segundo Nombre + Apellido
        ]

        pattern = '^' + '|'.join(patterns)

        result = re.match(pattern, s)

        if result :
            return True

        return False
