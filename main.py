import re
import regex
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def Main() :
    year = int(input('Año: '))
    month = int(input('Mes: '))
    is_grv = input('GRV? (y/n): ')
    if is_grv == 'n' :
        who = input('Quién?: ')
    else : 
        who = 'Relación Contabilidad'

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    #file_path = 'Chat de WhatsApp con Amorcito.txt'

    # region Chat_df
    parsed_data = [] 

    fp = open(file_path, 'r', encoding="utf-8")
    lines = fp.readlines()
    
    message_buffer = []
    for line in lines :
        line = line.replace('p. m.', 'PM').replace('a. m.', 'AM').replace('a.\xa0m.', 'AM')
        line = line.strip()
        if Start_With_Date_And_Time(line) : 
            if len(message_buffer) > 0 : 
                parsed_data.append([date_time, author, ' '.join(message_buffer)]) 
            message_buffer.clear() 
            date_time, author, message = Get_Data_Point(line)
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
    # endregion

    # region Accounty_df
    dates = []
    descriptions = []
    ingresos = []
    gastos = []

    for i in range(len(chat)) :
        if chat.index[i].year == year and chat.index[i].month == month :
            message = chat['Message'].values[i]
            category = Ingreso_Gasto(message)
            if category == 0 : continue
        
            message = message.replace('*', '')
            words = message.split(' ')

            sum = 0
            for word in words :
                if word.isnumeric() and int(word) >= 1000 :
                    sum += int(word)

            if category == 1 :
                gastos.append(sum)
                ingresos.append(0)
            elif category == 2 :
                gastos.append(0)
                ingresos.append(sum)
            elif category == 3 :
                gastos.append(0)
                ingresos.append(0)
            else : continue
            
            dates.append(chat.index[i])
            descriptions.append(message)
            
    accounty_df = pd.DataFrame()
    accounty_df['Fecha'] = np.array(dates)
    accounty_df['Descripcion'] = np.array(descriptions)
    accounty_df['Egresos'] = np.array(gastos)
    accounty_df['Ingresos'] = np.array(ingresos)
    # endregion

    saldo_anterior, nuevo_saldo, R2_ingresos = GRV_gastos(accounty_df)
    
    accounty_df.to_csv(f"{who} {month} {year}.csv")

    if who == 'Relación Contabilidad' :
        summary_df = pd.DataFrame(columns=['Concepto', 'Valor'])
        summary_df.loc[len(summary_df)] = ['Saldo anterior', saldo_anterior]
        summary_df.loc[len(summary_df)] = ['Nuevo Saldo', nuevo_saldo]
        summary_df.loc[len(summary_df)] = ['Ingreso GRV por R2', R2_ingresos]
        summary_df.to_csv(f"Resumen {month} {year}.csv")

    input('Presiona enter')

def Start_With_Date_And_Time(s) :
    pattern = "^\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}\S [AaPp][Mm] -"
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

def Get_Data_Point(line) :
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

def Ingreso_Gasto(description) :
    
    if description[:3] == '***' :    # Anotación
        return 3
    elif description[:2] == '**' :   # Ingreso
        return 2
    elif description[:1] == '*' :    # Gasto
        return 1
    else : return 0

def GRV_gastos(df) :

    saldo_anterior = int(input('Saldo GRV: '))
    R2_ingresos = int(input('Ingresos GRV por Roble2: '))

    cuenta_grv = 0
    for i in range(len(df)) :
        message = df['Descripcion'].values[i]
        words = message.split(' ')
        if words[0] == 'Grv' or words[0] == 'grv' :
            if df['Egresos'].values[i] != 0 :
                cuenta_grv -= df['Egresos'].values[i]
            elif df['Ingresos'].values[i] != 0 :
                cuenta_grv += df['Ingresos'].values[i]

    cuenta_grv += R2_ingresos

    nuevo_saldo = saldo_anterior + cuenta_grv

    return saldo_anterior, nuevo_saldo, R2_ingresos

Main()

# References:

# Arce, Luis Rafael. (2020). WhatsApp group chat analysis with python. Medium.
# Link: https://medium.com/mcd-unison/whatsapp-group-chat-analysis-with-python-3f5196280ba

# Sheriff, Samir. (2019). Build your own Whatsapp Chat Analyzer. Towards Data Science.
# Link: https://towardsdatascience.com/build-your-own-whatsapp-chat-analyzer-9590acca9014