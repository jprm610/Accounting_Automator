import re
import regex
import pandas as pd
import numpy as np
import datetime

def Main() :
    parsed_data = [] 

    conversation_path = 'chat.txt' 
    with open(conversation_path, encoding="utf-8") as fp:
        fp.readline() 
        message_buffer = [] 
        date_time, author = None, None
        while True:
            line = fp.readline() 
            if not line: 
                break
            line = line.strip() 
            if Start_With_Date_And_Time(line): 
                if len(message_buffer) > 0: 
                    parsed_data.append([date_time, author, ' '.join(message_buffer)]) 
                message_buffer.clear() 
                date_time, author, message = Get_Data_Point(line) 
                message_buffer.append(message) 
            else:
                message_buffer.append(line)
    
    chat = pd.DataFrame(parsed_data, columns=['Date_Time', 'Author', 'Message'])

    chat["Date_Time"] = pd.to_datetime(chat["Date_Time"])
    chat['date'] = [d.date() for d in chat['Date_Time']]
    del chat['Date_Time']

    chat.set_index('date', inplace=True)

    chat.to_csv('df_chat.csv')

def Start_With_Date_And_Time(s) :
    pattern = "^\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}\S [AaPp][Mm] -"
    result = re.match(pattern, s)

    if result :
        return True

    return False

def Find_Author(s) :
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

def Get_Data_Point(line):   
    split_line = line.split(' - ') 
    date_time = split_line[0]
    message = ' '.join(split_line[1:])
    if Find_Author(message): 
        split_message = message.split(': ') 
        author = split_message[0] 
        message = ' '.join(split_message[1:])
    else:
        author = None
    return date_time, author, message

Main()