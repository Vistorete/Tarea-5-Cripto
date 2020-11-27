import  imaplib, email, re, smtplib, datetime, time
from typing import List, Set, Dict, Tuple, Optional
from dateutil import parser

user = '' # usuario
password = ''    # contraseña
imap_url = ''     # servidor

















def set_connection(imap_url, user, password):
    """Establece la conexion con el correo

    Args:
        imap_url (str): Dirección del servidor de correos
        user (str): Cuenta del usuario
        password (str): Contraseña de la cuenta

    Returns:
        imaplib.IMAP4_SSL: Objeto que establece la conexion con el correo
    """
    imap = imaplib.IMAP4_SSL(imap_url)
    imap.login(user, password)
    return imap

def get_mail_regex_date(ruta):
    """Funcion que permite obtener el regex y el correo para filtrar

    Args:
        ruta (string): Ruta del archivo donde está el regex y correo

    Returns:
        list[tuple]: Lista de tuplas con los correos y su regex
    """
    file1 = open(ruta, 'r') 
    Lines = file1.readlines()
    list = []
    for line in Lines:
        elementos = line.split(",")
        elementos[-1] = elementos[-1].strip()
        elementos[-1] = parser.parse(elementos[-1])
        list.append(tuple(elementos))
        print(list)
    return list

def get_msg_id(imap, mail_address, file_path = None):
    """Obtiene las ID de los mensajes a partir de una dirección de correo

    Args:
        imap (imaplib.IMAP4_SSL): Objeto con el que se establecio la conexion
        mail_address (str): Direcion del mail para filtrar correos
        file_path (str, optional): direccion de archivo para guardar las IDs de los correos. Defaults to None.

    Returns:
        list[tuple(str,str)]: Lista de Tuplas que contiene el N° de correo y la ID
    """
    
    status, messages = imap.select('INBOX')
    print(f"{mail_address}\n\tObteniendo correos...")
    status, mails_id = imap.search(None,f'(FROM "{mail_address}")')
    mails_id=str(mails_id)[3:-2].rsplit(' ')
    msg_ids=[]
    if file_path:
        outFile=open('Message-IDs.txt','w')
    for id in mails_id:
        res,msg = imap.fetch(id,'(RFC822)')
        for msg_data in msg:
            if isinstance(msg_data,tuple):
                msg_= email.message_from_bytes(msg_data[1])
                if file_path:
                    outFile.write(msg_['Message-ID'][1:-1]+','+msg_['Date']+'\n')
                msg_ids.append((id,msg_['Message-ID'][1:-1],msg_['Date']))
    if file_path:
        outFile.close()
    print(f'{mail_address}:\n\ttotal de correos obtenidos:{len(msg_ids)}')
    return msg_ids

def check_regex(msgs_id, regular_expression, date):
    """Compara la fecha de los correos y la ID con una expresion regular

    Args:
        msgs_id list[tuple(str,str)]: [description]
        regular_expression (str): Expresion regular con la que se compara
        date (datetime): Fecha con la que se compara
    """
    
    for element in msgs_id:
        mail_date = parser.parse(element[-1]).date()
        if mail_date > date.date():
            print("Regex posiblemente desactualizada para:", element)
        elif re.search(regular_expression, element[1]):
            print("Aprobada:", element)
        else:
            print("Posible suplantación de identidad:", element)
    pass


if __name__ == "__main__":

    
    imap = set_connection(imap_url, user, password) # establece la conexion
    mail_regex = get_mail_regex_date('correos_regex.txt') # obtiene la expresion rgular desde un archivo
    for elemento in mail_regex: # Por cada expresion regular 
        msg_ids = get_msg_id(imap, elemento[0]) # Por cada elemento entrega la direccion
        check_regex(msg_ids, elemento[1], elemento[2]) # Entrega los mensajes con ID, la expresion regular y la fecha de la expresion



