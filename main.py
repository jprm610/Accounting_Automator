import re
import regex
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import plotly as py
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.graph_objs import *

def Main() :
    year = int(input('Año: '))
    month = int(input('Mes: '))

    root = tk.Tk()
    root.withdraw()

    #file_path = filedialog.askopenfilename()

    file_path = 'Chat de WhatsApp con Amorcito.txt'

    # region Chat_df
    parsed_data = [] 

    fp = open(file_path, 'r', encoding="utf-8")
    lines = fp.readlines()
    
    message_buffer = []
    for line in lines :
        line = line.replace('\u202f', ' ')
        line = line.replace('p. m.', 'PM').replace('a. m.', 'AM')
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

            message = Normalize(message)
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

    conceptos = Summary_Data(accounty_df)
    
    accounty_df.to_csv(f"Relación Contabilidad {month} {year}.csv")

    # region Summary_df
    summary_df = pd.DataFrame(conceptos.items(), columns=['Concepto', 'Valor'])

    summary_df.to_csv(f"Resumen {month} {year}.csv")
    # endregion

    Analysis(accounty_df, conceptos['Saldo anterior GRV'])

    input('Presiona enter')

def Start_With_Date_And_Time(s) :
    pattern = "^\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{1,2}\S [AaPp][Mm] -"
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

def Summary_Data(df) :

    saldo_anterior = int(input('Saldo GRV: '))
    R2_ingresos = int(input('Ingresos GRV por Roble2: '))
    conceptos = {
        'Saldo anterior GRV': saldo_anterior,
        'Ingreso GRV por R2': R2_ingresos,
        'Nuevo Saldo GRV': 0,
        'Jornales': 0,
        'Caja menor': 0,
        'Pila': 0,
        'Creditos': 0,
        'Intereses': 0,
        'Roble2': 0,
        'Prestamos': 0,
        'Contabilidad': 0,
        'El Corozo': 0,
        'Casa Palestina': 0
    }

    cuenta_grv = 0
    for i in range(len(df)) :
        message = df['Descripcion'].values[i]
        words = message.split(' ')
        if words[0] == 'GRV' :
            if df['Egresos'].values[i] != 0 :
                cuenta_grv -= df['Egresos'].values[i]
            elif df['Ingresos'].values[i] != 0 :
                cuenta_grv += df['Ingresos'].values[i]
        elif (words[0] == 'JORNALES' or 
            (words[0] == 'R2' and words[1] == 'JORNALES')) :
            conceptos['Jornales'] += df['Egresos'].values[i]
        elif words[0] == 'R2' :
            conceptos['Roble2'] += df['Egresos'].values[i]
        elif (words[0] == 'CAJA' and words[1] == 'MENOR') :
            conceptos['Caja menor'] += df['Egresos'].values[i]
        elif words[0] == 'PILA' :
            conceptos['Pila'] += df['Egresos'].values[i]
        elif words[0] == 'CREDITO' :
            conceptos['Creditos'] += df['Egresos'].values[i]
        elif words[0] == 'INTERESES' :
            conceptos['Intereses'] += df['Egresos'].values[i]
        elif words[0] == 'PRESTAMO' :
            conceptos['Prestamos'] += df['Egresos'].values[i]
        elif words[0] == 'CONTABILIDAD' :
            conceptos['Contabilidad'] += df['Egresos'].values[i]
        elif words[0] == 'EL' and words[1] == 'COROZO' :
            conceptos['El Corozo'] += df['Egresos'].values[i]
        elif words[0] == 'ROSITA' and words[1] == 'PALESTINA' :
            conceptos['Casa Palestina'] += df['Egresos'].values[i]

    cuenta_grv += R2_ingresos

    conceptos['Nuevo Saldo GRV'] = saldo_anterior + cuenta_grv

    return conceptos

def Normalize(s:str) :
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
    
    return s

def Analysis(df, saldo_anterior) :
    dates = []
    descr = []
    values = []

    for i in range(len(df)) :
        value = 0
        dates.append(df['Fecha'].values[i])
        descr.append(df['Descripcion'].values[i])
        value -= df['Egresos'].values[i]
        value += df['Ingresos'].values[i]
        values.append(value)

    condenced_df = pd.DataFrame({
        'Fecha': np.array(dates),
        'Descripcion': np.array(descr),
        'Valor': np.array(values)
    })

    acum_df = pd.DataFrame({
        'Fecha': np.array(dates),
        'Descr': np.array(descr),
        'Acumulado': np.cumsum(condenced_df['Valor'])
    })
    
    gen = make_subplots(rows=1, cols=1, shared_xaxes=True)

    gen.add_trace(
        go.Scatter(x=acum_df['Fecha'], y=acum_df['Acumulado'], 
        line=dict(color='rgba(26,148,49)', width=1),
        fill='tozeroy'),
        row=1, col=1
    )

    gen.update_layout(paper_bgcolor='rgba(0,0,0)', plot_bgcolor='rgba(0,0,0)')

    py.offline.plot(gen, filename = "Evolución_General.html")

    grv_dates = []
    grv_values = []
    grv_descr = []
    for i in range(len(condenced_df)) :
        message = condenced_df['Descripcion'].values[i]
        words = message.split(' ')
        if words[0] == 'Grv' :
            grv_dates.append(condenced_df['Fecha'].values[i])
            grv_descr.append(condenced_df['Descripcion'].values[i])
            grv_values.append(condenced_df['Valor'].values[i])

    grv_df = pd.DataFrame({
        'Fecha': np.array(grv_dates),
        'Descr': np.array(grv_descr),
        'Valor': np.array(grv_values)
    })

    grv_acum_df = pd.DataFrame({
        'Fecha': np.array(grv_dates),
        'Descr': np.array(grv_descr),
        'Acumulado': np.cumsum(grv_df['Valor'])
    })

    grv_acum_df['Acumulado'] = grv_acum_df['Acumulado'].apply(lambda x: x + saldo_anterior)
    
    grv = make_subplots(rows=1, cols=1, shared_xaxes=True)

    grv.add_trace(
        go.Scatter(x=grv_acum_df['Fecha'], y=grv_acum_df['Acumulado'], 
        line=dict(color='rgba(26,148,49)', width=1),
        fill='tozeroy'),
        row=1, col=1
    )

    grv.update_layout(paper_bgcolor='rgba(0,0,0)', plot_bgcolor='rgba(0,0,0)')

    py.offline.plot(grv, filename = "Evolución_GRV.html")

Main()

# References:

# Arce, Luis Rafael. (2020). WhatsApp group chat analysis with python. Medium.
# Link: https://medium.com/mcd-unison/whatsapp-group-chat-analysis-with-python-3f5196280ba

# Sheriff, Samir. (2019). Build your own Whatsapp Chat Analyzer. Towards Data Science.
# Link: https://towardsdatascience.com/build-your-own-whatsapp-chat-analyzer-9590acca9014