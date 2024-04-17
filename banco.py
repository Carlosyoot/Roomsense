import sqlite3;import yaml;import re;import streamlit as st;import time
import pandas as pd;import smtplib;
from markdowncss import *
from dateutil.rrule import rrule, WEEKLY
from pyngrok import ngrok
import datetime
from datetime import date

def verificar_lembretes():
    
    with sqlite3.connect("database/meetingdatabase.db") as conn:
        
        try:
            
            cursor = conn.cursor()
            
            agora = datetime.datetime.now()
            
            hora_lembrete = datetime.timedelta(hours=24)
            
            hora_lembrete_antes = agora + hora_lembrete
            
            
            cursor.execute("SELECT * FROM currentmeeting WHERE data <= ? AND data >= ?",
                           (hora_lembrete_antes.strftime('%Y-%m-%d'), agora.strftime('%Y-%m-%d')))
            
            reunioes_para_lembrete = cursor.fetchall()

            for reuniao in reunioes_para_lembrete:
                
                if reuniao[10] == 0:
                    
                    participantes = reuniao[8].split(',') 
                    
                    for participante in participantes:
                        
                        destinatario = enviar(participante)
                        
                        nomereuniao = reuniao[3]
                        
                        data = reuniao[2]
                        
                        horainicioform = reuniao[6]
                        
                        horasfimform = reuniao[7]
                        
                        salas_sem_aspas = reuniao[9]
                        
                        organizador = reuniao[4]
                        
                        
                        enviar_email_recorrente(destinatario, nomereuniao, data, horainicioform, horasfimform, salas_sem_aspas, organizador)

                    # Atualizar o campo email_enviado para indicar que o e-mail foi enviado
                        cursor.execute("UPDATE currentmeeting SET Booleanemail = 1 WHERE id = ?", (reuniao[0],))
                else:
                    print('nenhuma reuniao sem enviar email')
            conn.commit()  # Confirmar as alterações no banco de dados

        except Exception as e:
            print(f"Erro ao verificar lembretes: {e}")

            
            
            
def criar_banco_dados():
    try:
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS meetingdatabase(
                id PRIMARY KEY,
                Assunto TEXT NOT NULL,
                Data TEXT NOT NULL,
                NomeReuniao TEXT NOT NULL,
                Organizador TEXT NOT NULL,
                Comentarios TEXT,
                HoraStart INTEGER NOT NULL,
                HoraEnd INTEGER NOT NULL,
                Participantes TEXT NOT NULL,
                Sala TEXT NOT NULL)''')
            print('Tabela de usuários criada com sucesso!')

            conn.commit()
    except sqlite3.Error as e:
        print("Erro ao criar tabela de usuários:", e)
        
        
def minchar():
    min = re.match(r'')


def splitname(username):
    try:
        consult = re.match(r'([^@]+)@', username)
        
        if consult:
            username = consult.group(1)
            
            if '.' in username:
                diviser = username.split('.')
                firstname = diviser[0].capitalize()
                lastname = diviser[-1].capitalize()
            else:
                firstname = username[:10].capitalize()
                lastname = ''
            
            return firstname, lastname
        else:
            return None, None
    except Exception as e:
        print("Erro ao dividir o nome:", e)
        
        
def inserir_usuario(username, email='', Permission='', password='123', login=False):
    
    
    try:
        
        with sqlite3.connect('database/usersdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            if username is not None and email != '' and Permission != '' and password != '123':
                
                firstname, lastname = splitname(username)
                
                cursor.execute("INSERT INTO usuarios (username, nameuser, email, login, Permission, password) VALUES (?, ?, ?, ?, ?, ?)",
                               (username, f"{firstname} {lastname}", email, login, Permission, password))
                
                print('Usuário inserido com sucesso!')
            
                conn.commit()

                dump_para_yaml()
    

            elif username is not None and Permission != '':
                
                firstname, lastname = splitname(username)
                
                cursor.execute("INSERT INTO usuarios (username, nameuser, email, login, Permission, password) VALUES (?, ?, ?, ?, ?, ?)",
                               (username, f"{firstname} {lastname}", username, login, Permission, password))
            
                print('Usuário inserido com sucesso!')

                conn.commit()

                dump_para_yaml()
    
    except sqlite3.Error as e:
        print("Erro ao inserir usuário:", e)


def dump_para_yaml():
    try:
        
        with sqlite3.connect('database/usersdatabase.db') as conn:
            
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios")
            
            userselect = cursor.fetchall()

            cursor.execute("SELECT * FROM cookies")
            cookieselect = cursor.fetchall()

            database = {'credentials': {'usernames': {}}, 'cookies': {}}

            for usuarioinsert in userselect:
                username, nameuser,email, login, Permission, password = usuarioinsert
                database['credentials']['usernames'][username] = {
                    'name': nameuser,
                    'email': email,
                    'logged': login,
                    'permission': Permission,
                    'password': password
                }

            for cookieinsert in cookieselect:
                name, key, expiry_days = cookieinsert
                database['cookies'] = {
                    'expiry_days': expiry_days,
                    'key': key,
                    'name': name,
                }

            with open('config.yaml', 'w') as file:
                yaml.dump(database, file, default_flow_style=False)

                print("Dump concluído com sucesso!")
    except sqlite3.Error as e:
        print("Erro ao realizar dump para YAML:", e)

def databaseuser(username):
    try:
        with sqlite3.connect('database/usersdatabase.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT nameuser, email, Permission FROM usuarios WHERE username=?", (username,))
            
            selecteduser = cursor.fetchone()
            
            if selecteduser:
                
                return {'nameuser': selecteduser[0], 'email': selecteduser[1],    'Permission': selecteduser[2]}
            
            else:
                
                return None
    except sqlite3.Error as e:
        
        print("Erro ao executar consulta SQL:", e)
        
        return None
    
def validate(email):
    
    default = re.compile(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$')
    
    if default.match(email):
        
        return True
    
    else:
        return False

def updatedataemail(username, newemail):

    try:
        
        toastmessage()
        
        if not validate(newemail):
            
            st.toast("Erro ao alterar o email.	:x:")
                    
            time.sleep(2)
            
            st.toast("O email não está em um formato válido.")
            
            
            return False

        with sqlite3.connect('database/usersdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
            
            databaseselect = cursor.fetchone()
            
            if databaseselect:
                
                cursor.execute("SELECT * FROM usuarios WHERE email=?", (newemail,))
                
                users = cursor.fetchone()
                
                if users and users[0] != username:
                    
                    st.toast("Erro ao alterar o email.	:x:")
                    
                    time.sleep(1)
                    
                    st.toast("Este email já está em uso.")
                    
                    return False
                
                if databaseselect[2] == newemail:
                    
                    st.toast("Erro ao alterar o email.")
                    
                    time.sleep(1)
                    
                    st.toast("O email atual é o mesmo que o email existente.")
                    
                    return False
                
                cursor.execute("UPDATE usuarios SET email=?, WHERE username=?", (newemail, username))
    
                conn.commit()
                
                dump_para_yaml()
                
                
                return True
            
            else:
                
                st.toast("Usuário não encontrado.")
                
                return False, None
    
    except sqlite3.Error as e:
        
        print("Erro ao alterar o email: {}".format(e))
        
        return False, None
    
def resetpassword(username, newpassword):
    try:
        with sqlite3.connect('database/usersdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
            
            userdatabase = cursor.fetchone()
            
            if userdatabase:
                
                cursor.execute("UPDATE usuarios SET password=? WHERE username=?", (newpassword, username))
                
                conn.commit()
                
                dump_para_yaml()
                
                return True
            
            else:
                
                st.toast("Usuario não encontrado :x:")
                
                time.sleep(2)
                
                return False
            
    except sqlite3.Error as e:
        
        print("Erro ao redefinir a senha:", e)
        
        return False
    
def verify(username):
    
    try:
        
        with sqlite3.connect('database/usersdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM usuarios WHERE email=?", (username,))
            
            result = cursor.fetchone()
            
            if result is not None:
                
                return True
            
            else:
                
                return False
            
    except sqlite3.Error as e:
        
        print("Erro ao verificar o email:", e)
        
    
@st.cache_data(show_spinner=True)        
def verifyroom(Roomname):
    
    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Rooms WHERE salas=?", (Roomname,))
            
            result = cursor.fetchone()
            
            if result is not None:
                
                return True
            
            else:
                
                return False
            
    except sqlite3.Error as e:
        
        print("Erro ao verificar sala:", e)
    
@st.cache_data(show_spinner=True)       
def inserirsala(Roomname):
    
    with sqlite3.connect('database/meetingdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Rooms (salas) VALUES (?)", (Roomname,))
            
            conn.commit()      
            
        except sqlite3.Error as e:
            
                print("Erro ao cadastrar sala:", e)
                
    
def getallusers():
    
    with sqlite3.connect('database/usersdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT nameuser FROM usuarios")
            
            result = cursor.fetchall()
            
            return [result[0] for result in result]
        
        except sqlite3.Error as e:
            
            print("Erro ao recuperar usuários:", e)
            
     
def getallrooms():
    
    with sqlite3.connect('database/meetingdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT salas FROM Rooms")
            
            result = cursor.fetchall()
            
            return [result[0] for result in result]

        except sqlite3.Error as e:
            
            print("Erro ao recuperar salas:", e)
            
def eventos():
    
    with sqlite3.connect('database/meetingdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM meetingdatabase")
            
            eventos = cursor.fetchall()
            
            return eventos
        
        except sqlite3.Error as e:
            
            print("Erro ao recuperar eventos:", e)
            
def eventosrecorrentes():
    
    with sqlite3.connect('database/meetingdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM currentmeeting")
            
            eventoscurrent = cursor.fetchall()
            
            return eventoscurrent
        
        except sqlite3.Error as e:
            
            print("Erro ao recuperar eventos recorrentes:", e)
            
        
def insertalert(usuario, mensagem):
   with sqlite3.connect('database/meetingdatabase.db') as conn:
        
        try:
            
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO alerts (usuarios, alert) VALUES (?,?)", (usuario, mensagem))
            
            conn.commit()  
            
        except sqlite3.Error as e:
            
                print("Erro ao cadastrar mensagem:", e)
                
    
def verificar_mensagens():
    
    username = st.session_state.get('username')
    
    mensagens, total_mensagens = recovery(username)
    
    if mensagens:
        
        st.markdown('''<style>
                        [data-testid="stExpander"][class="st-emotion-cache-0 eqpbllx5"]{
                            margin-top: 40px;
                        }
                    </style>''', unsafe_allow_html=True)
        
        with st.expander(f"Mensagens **({total_mensagens})**", expanded=True):
            
            for i, mensagem in enumerate(mensagens, start=1):
                
                st.write(f"{i} - {mensagem}", unsafe_allow_html=True)
    else:
        
        st.markdown('''<style>
                        [data-testid="stExpander"][class="st-emotion-cache-0 eqpbllx5"]{
                            margin-top: 40px;
                        }
                    </style>''', unsafe_allow_html=True)
        
        with st.expander(f"Mensagens **({total_mensagens})**", expanded=True):
            
            st.write("Nenhuma mensagem encontrada.")


def recovery(username):

    try:
    
        with sqlite3.connect('database/meetingdatabase.db') as conn:
        
            cursor = conn.cursor()
        
            cursor.execute("SELECT alert FROM alerts WHERE usuarios=?", (username,))
        
            mensagens = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE usuarios=?", (username,))
            
            total_mensagens = cursor.fetchone()[0]
            
            return [mensagem[0] for mensagem in mensagens], total_mensagens
        
        
    except sqlite3.Error as e:
        
        print("Erro ao recuperar mensagens:", e)
        
def alertclean(username):
    with sqlite3.connect('database/meetingdatabase.db') as conn:
        try:
            cursor = conn.cursor()    
            cursor.execute("DELETE FROM alerts WHERE usuarios=?", (username,))
            conn.commit()
            return st.rerun()
                
        except sqlite3.Error as e:
            print("Erro ao limpar mensagens:", e)
            

@st.cache_resource(show_spinner=True)            
def insertmeeting(assunto, data, nomereuniao, comentarios, horasinicio, horasfim, participantes, roomsalas):
    
    organizador = st.session_state.get('name')  
    
    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO meetingdatabase (assunto, data, nomereuniao, organizador, comentarios, HoraStart, HoraEnd, Participantes, Sala) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (assunto, data, nomereuniao, organizador, comentarios, horasinicio, horasfim, participantes, roomsalas)
            )

            conn.commit()
            
            
            
    except sqlite3.Error as e:
        
        st.error("Erro ao agendar reunião:", e)
        
    
@st.cache_resource(show_spinner=True)
def insert_recurring_meetings(assunto, data, data_final, nomereuniao, comentarios, horasinicio, horasfim, participantes, roomsalas, regra_recorrencia):
    
    organizador = st.session_state.get('name')
    
    dias_da_semana = {
        'Segunda-feira': 0,
        'Terça-feira': 1,
        'Quarta-feira': 2,
        'Quinta-feira': 3,
        'Sexta-feira': 4,
    }

    dia_da_semana_numero = dias_da_semana[regra_recorrencia]

    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            if isinstance(data, date):
                
                data = datetime.combine(data, datetime.min.time())
            
            # Inserir a primeira reunião na data inicial
            cursor.execute(
                "INSERT INTO currentmeeting (assunto, data, nomereuniao, organizador, comentarios, HoraStart, HoraEnd, Participantes, Sala) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (assunto, data.strftime('%Y-%m-%d'), nomereuniao, organizador, comentarios, horasinicio, horasfim, participantes, roomsalas)
            )
            
            # Gerar as datas de recorrência a partir da próxima ocorrência da regra
            
            for dt in rrule(WEEKLY, dtstart=data, until=data_final, byweekday=dia_da_semana_numero):
                # Verificar se a data é após a data inicial
                if dt.date() > data.date():
                    
                    dtslipped = dt.strftime('%Y-%m-%d')
                    
                    cursor.execute(
                        "INSERT INTO currentmeeting (assunto, data, nomereuniao, organizador, comentarios, HoraStart, HoraEnd, Participantes, Sala) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (assunto, dtslipped, nomereuniao, organizador, comentarios, horasinicio, horasfim, participantes, roomsalas)
                    )

            conn.commit()
            
            st.success("Reuniões recorrentes agendadas com sucesso!")
            
    except sqlite3.Error as e:
        
        print("erro ao inserir reunião recorrente: ", e)
   
      
def relatorios(tabela1, tabela2):
    
    conn = sqlite3.connect('database/meetingdatabase.db')

    
    query1 = f"SELECT * FROM {tabela1}"
    
    df1 = pd.read_sql_query(query1, conn)

    
    query2 = f"SELECT * FROM {tabela2}"
    
    df2 = pd.read_sql_query(query2, conn)

    
    conn.close()

    
    df_combined = pd.concat([df1, df2])

    df_combined.to_csv('database/relatorios.csv', index=False)
    

@st.cache_resource(show_spinner=True)
def enviar(username):
    
    with sqlite3.connect('database/usersdatabase.db') as conn:
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT email FROM usuarios WHERE nameuser COLLATE NOCASE = ?", (username,))
        
        resultselect = cursor.fetchone()
        
        if resultselect is not None:
            
            return resultselect[0]
        
        else:
            
            print("Email não encontrado para o usuário:", username)
            
@st.cache_data(show_spinner=True,persist=True)
def enviar_email(destinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas,organizador):
    
    from email.mime.multipart import MIMEMultipart
    
    from email.mime.text import MIMEText
    
    
    data_str = data.strftime("%Y-%m-%d")

    dataformatada = datetime.datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    public_url = None
    
    if public_url == None:
       
        public_url = start_ngrok()
    
    
    corpo_email = """
    <div style="margin: 0 auto; max-width: 600px; border: 1px solid rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;justify-content: center;">
    <div style="background-color: #f2f2f2; padding: 5px; border-bottom: 1px solid rgba(0, 0, 0, 0.1);">
        <p style="font-size: 18px; color:#0F248D;"><b>Onboard {} </b></p>
    </div>
    <div style="color:#000000; padding-top: 10px;">
        <p style="font-weight: bold;">Olá, você foi convidado para participar de uma reunião.</p>
        <p><b>Data: </b> {} <b> Horas: </b> {} - {} <b> Sala: </b>{}</p>
        <p><b>Organizador: </b> {} </p>
        <p>Confirme sua presença</p>
    </div>
    <div style="display: flex ;justify-content: center; padding-top: 10px; align-items: center;">
        <div style="margin-right: 10px; margin: 0 auto;">
            <div><a href="{}/confirmacaoA/{}/A/{}" style="background-color: #4CAF50; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Confirmar presença</a></div>
        </div>
        <div style="margin-right: 10px; margin: 0 auto;">
            <div><a href="{}/confirmacaoB/{}/B/{}" style="background-color: #D20103; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Não confirmar</a></div>
        </div>
    </div>
    <div dir="ltr" style="padding-top: 10px; position: relative;">
    <br clear="all">
    <span class="gmail_signature_prefix"></span>
    <br>
    <div dir="ltr" class="gmail_signature" data-smartmail="gmail_signature">
        <div dir="ltr">
            <img src="https://www.fortics.com.br/wordpress/wp-content/uploads/2021/11/IAra_100x100-980x980-compress.png" width="94" height="96" style="margin: 0 auto;"><br>
        </div>
    </div>
    <p style="font-size: 12px; text-align: center;">Fortics © 2024 Onboard. Todos os direitos reservados.</p>
</div>
""".format(nomereuniao, dataformatada, horainicioform, horasfimform, salas_sem_aspas, organizador, public_url,destinatario,data,public_url, destinatario,data)




    msg = MIMEMultipart('alternative')
    
    msg['Subject'] = "Reunião agendada"
    
    msg['From'] = 'notificationroomsense@gmail.com' 
    
    msg['To'] = destinatario
    
    password = 'eglvofathkkrmlea'
     
    msg.attach(MIMEText(corpo_email, 'html'))

    s = smtplib.SMTP('smtp.gmail.com: 587')
    
    s.starttls()
    
    s.login(msg['From'], password)
    
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    s.quit()
    
@st.cache_data(show_spinner=True,persist=True)
def enviar_email_recorrente(destinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas,organizador):
    
    from email.mime.multipart import MIMEMultipart
    
    from email.mime.text import MIMEText
    
    data_str = data.strftime("%Y-%m-%d")

    dataformatada = datetime.datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    public_url = None
    
    if public_url == None:
       
        public_url = start_ngrok()
    
    
    corpo_email = """
    <div style="margin: 0 auto; max-width: 600px; border: 1px solid rgba(0, 0, 0, 0.1); padding: 10px; text-align: center;justify-content: center;">
    <div style="background-color: #f2f2f2; padding: 5px; border-bottom: 1px solid rgba(0, 0, 0, 0.1);">
        <p style="font-size: 18px; color:#0F248D;"><b>Onboard {} </b></p>
    </div>
    <div style="color:#000000; padding-top: 10px;">
        <p style="font-weight: bold;">Olá, passando um lembrete sobre uma reunião recorrente!.</p>
        <p><b>Data: </b> {} <b> Horas: </b> {} - {} <b> Sala: </b>{}</p>
        <p><b>Organizador: </b> {} </p>
        <p>Confirme sua presença</p>
    </div>
    <div style="display: flex ;justify-content: center; padding-top: 10px; align-items: center;">
        <div style="margin-right: 10px; margin: 0 auto;">
            <div><a href="{}/confirmacaoA/{}/A/{}" style="background-color: #4CAF50; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Confirmar presença</a></div>
        </div>
        <div style="margin-right: 10px; margin: 0 auto;">
            <div><a href="{}/confirmacaoB/{}/B/{}" style="background-color: #D20103; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Não confirmar</a></div>
        </div>
    </div>
    <div dir="ltr" style="padding-top: 10px; position: relative;">
    <br clear="all">
    <span class="gmail_signature_prefix"></span>
    <br>
    <div dir="ltr" class="gmail_signature" data-smartmail="gmail_signature">
        <div dir="ltr">
            <img src="https://www.fortics.com.br/wordpress/wp-content/uploads/2021/11/IAra_100x100-980x980-compress.png" width="94" height="96" style="margin: 0 auto;"><br>
        </div>
    </div>
    <p style="font-size: 12px; text-align: center;">Fortics © 2024 Onboard. Todos os direitos reservados.</p>
</div>
""".format(nomereuniao, dataformatada, horainicioform, horasfimform, salas_sem_aspas, organizador, public_url,destinatario,data,public_url, destinatario,data)




    msg = MIMEMultipart('alternative')
    
    msg['Subject'] = "Lembrete de reunião"
    
    msg['From'] = 'notificationroomsense@gmail.com' 
    
    msg['To'] = destinatario
    
    password = 'eglvofathkkrmlea'
     
    msg.attach(MIMEText(corpo_email, 'html'))

    s = smtplib.SMTP('smtp.gmail.com: 587')
    
    s.starttls()
    
    s.login(msg['From'], password)
    
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

    s.quit()

    
def start_ngrok():
    public_url = ngrok.connect(5000).public_url
    return public_url


def requestuser():
    
    try:
        
        with sqlite3.connect("mailer/respostas.db") as conn:
            
            cursor = conn.cursor()
            
            result = cursor.execute("SELECT id, email, resposta, data FROM respostas Where resposta = 'B'")
            
            dados = result.fetchall()
            
            return dados
        
    except sqlite3.Error as e:
        
        print("Erro ao recuperar respostas:", e)
        
def confirmuser():
    
    try:
        
        with sqlite3.connect("mailer/respostas.db") as conn:
            
            cursor = conn.cursor()
            
            result = cursor.execute("SELECT email, resposta, data FROM respostas Where resposta = 'A'")
            
            dados = result.fetchall()
            
            return dados
        
    except sqlite3.Error as e:
        
        print("Erro ao recuperar respostas:", e)

def remove_participant(email, data):
    
    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            cursor = conn.cursor()
            
            participantea = requestusername(email)
            
            id_reuniao = get_meeting_id(participantea, data)
            
            
            cursor.execute("SELECT Participantes FROM meetingdatabase WHERE id = ? AND Data = ?", (id_reuniao, data))
            
            participantes_row = cursor.fetchone()
            
            if participantes_row:
                
                participantes = participantes_row[0]
                
                participantes_lista = participantes.split(', ')
                
                participantes_lista.remove(participantea)
                
                participantes_atualizados = ', '.join(participantes_lista)
                
                cursor.execute("UPDATE meetingdatabase SET Participantes = ? WHERE id = ? AND Data = ?", (participantes_atualizados, id_reuniao, data))
                
                remove_response(email, data)
                
                conn.commit()
                
                retorno = cursor.execute("SELECT organizador FROM meetingdatabase WHERE id = ?", (id_reuniao,))
                
                
                organizador_row = retorno.fetchone()
                
                
                if organizador_row:
                    
                    
                    organizador = organizador_row[0]
                    
                    
                    organizador1 = enviar(organizador)
                    
                    import datetime
                    
                    dataformatada = datetime.datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    
                    
                    mensagem = '<span>O participante <span style=" font-weight: bold; color: blue;">{}</span><span> cancelou sua participação na reunião na data de </span><span style=" font-weight: bold">{}</span>.</span>'.format(participantea, dataformatada)
                    
                    insertalert(organizador1, mensagem)
                    
        
                else:
                    print("Organizador não encontrado para a reunião.")
                
            else:
                
                print("Reunião não encontrada para o participante e data fornecidos.")
                
                remove_response(email, data)
    
                
    except sqlite3.Error as e:
        
        print("Erro ao remover usuário da lista de participantes:", e)

        


def requestusername(email):
    
    try:
        
        with sqlite3.connect("database/usersdatabase.db") as conn:
            
            cursor = conn.cursor()
            
            
            
            result = cursor.execute("SELECT nameuser FROM usuarios WHERE email = ?", (email,))
            
            user = result.fetchone()

            if user:
                
                return user[0]
            
            else:
                
                return None

    except sqlite3.Error as e:
        
        print("Erro ao recuperar nome do usuário:", e)
        
def remove_response(email, data):
    
    try:
        
        with sqlite3.connect("mailer/respostas.db") as conn:
            
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM respostas WHERE email = ? AND data = ?", (email, data))
            
            conn.commit()
             

    except sqlite3.Error as e:
        
        print("Erro ao remover resposta do usuário:", e)
        
def get_meeting_id(email, data):
    
    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM meetingdatabase WHERE Data = ? AND Participantes LIKE ?", (data, f'%{email}%'))
            
            row = cursor.fetchone()
            
            if row:
                
                return row[0]
              
            else:
                
                return None 
            
    except sqlite3.Error as e:
        
        print("Erro ao obter a ID da reunião:", e)
        
        return None


def tip():
    with sqlite3.connect('database/usersdatabase.db') as conn:
        try:
            cursor = conn.cursor()
            
            user = st.session_state["username"]
            
            cursor.execute('SELECT Permission FROM usuarios WHERE username = ?', (user,))
            
            userprivilege = cursor.fetchone()
            
            return userprivilege[0]
        
        except sqlite3.Error as e:
            print("Erro ao recuperar privilegios:", e)
    
def get_all_meetings():
    all_meetings = []

    with sqlite3.connect('database/meetingdatabase.db') as conn:
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, NomeReuniao, Participantes FROM currentmeeting")
            meetings_recurrent = cursor.fetchall()
        
            for meeting in meetings_recurrent:
                meeting_info = {
                    "Id": meeting[0],
                    "Nome": meeting[1],
                    "Participantes": meeting[2]
                }
                all_meetings.append(meeting_info)
            
            cursor.execute("SELECT id, NomeReuniao, Participantes FROM meetingdatabase")
            
            meetings_unique = cursor.fetchall()
            
            for meeting in meetings_unique:
                meeting_info = {
                    "Id": meeting[0],
                    "Nome": meeting[1],
                    "Participantes": meeting[2]
                }
                all_meetings.append(meeting_info)
            
        except sqlite3.Error as e:
            print("Erro ao recuperar reuniões:", e)
    
    return all_meetings

def update_meeting(meeting_id, data, nomereuniao, horasinicio, horasfim, participantes, salas, motivo):
    try:
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            cursor = conn.cursor()

            update_fields = []  
            update_values = []  

   
            if data is not None:
                update_fields.append("data=?")
                update_values.append(data)
            if nomereuniao is not None:
                update_fields.append("nomereuniao=?")
                update_values.append(nomereuniao)
            if horasinicio is not None:
                update_fields.append("HoraStart=?")
                update_values.append(horasinicio)
            if horasfim is not None:
                update_fields.append("HoraEnd=?")
                update_values.append(horasfim)
            if participantes is not None:
                update_fields.append("Participantes=?")
                update_values.append(participantes)
            if salas is not None:
                update_fields.append("Sala=?")
                update_values.append(salas)
            if motivo is not None:
                update_fields.append("comentarios=?")
                update_values.append(motivo)

          
            update_query = "UPDATE meetingdatabase SET {} WHERE id=?".format(", ".join(update_fields))

            
            update_values.append(meeting_id)

           
            cursor.execute(update_query, update_values)

        
            if cursor.rowcount == 0:  
                cursor.execute("""
                    UPDATE currentmeeting
                    SET {}
                    WHERE id=?
                """.format(", ".join(update_fields)), update_values)

                if cursor.rowcount == 0: 
                    st.warning("Reunião não encontrada.")
                else:
                    conn.commit()
                    st.success("Reunião atualizada com sucesso!")
                    time.sleep(2)
            else:
                conn.commit()
                st.success("Reunião atualizada com sucesso!")
                time.sleep(2)
            
    except sqlite3.Error as e:
        
        print("Erro ao atualizar reunião:", e)

        
def delete_meeting(meeting_id):
    try:
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM meetingdatabase WHERE id = ?", (meeting_id,))
            
            if cursor.rowcount == 0:
                
                cursor.execute("DELETE FROM currentmeeting WHERE id = ?", (meeting_id,))
            else:
                conn.commit()
                
                st.success("Reunião excluída com sucesso!")
                
            
    except sqlite3.Error as e:
        st.error("Erro ao excluir reunião:", e)
        
import sqlite3

def get_meeting_data_by_id(meeting_id):
    
    try:
        
        with sqlite3.connect('database/meetingdatabase.db') as conn:
            
            cursor = conn.cursor()
            

            cursor.execute("SELECT Id, Data, NomeReuniao, HoraStart, HoraEnd, Participantes, Sala, Comentarios FROM meetingdatabase WHERE id=?", (meeting_id,))
            
            meeting_data = cursor.fetchone()

            if meeting_data:
                meeting_info = {
                    "Id": meeting_data[0],
                    "Data": meeting_data[1],
                    "NomeReuniao": meeting_data[2],
                    "HoraStart": meeting_data[3],
                    "HoraEnd": meeting_data[4],
                    "Participantes": meeting_data[5],
                    "Sala": meeting_data[6],
                    "Comentarios": meeting_data[7]
                }
                return meeting_info
            else:
                cursor.execute("SELECT Id, Data, NomeReuniao, HoraStart, HoraEnd, Participantes, Sala, Comentarios FROM currentmeeting WHERE id=?", (meeting_id,))
                meeting_data = cursor.fetchone()

                if meeting_data:
                    meeting_info = {
                        "Id": meeting_data[0],
                        "Data": meeting_data[1],
                        "NomeReuniao": meeting_data[2],
                        "HoraStart": meeting_data[3],
                        "HoraEnd": meeting_data[4],
                        "Participantes": meeting_data[5],
                        "Sala": meeting_data[6],
                        "Comentarios": meeting_data[7]
                    }
                    return meeting_info
                else:
                    return None
    except sqlite3.Error as e:
        print("Erro ao buscar os dados da reunião:", e)
        return None

