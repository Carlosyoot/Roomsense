import streamlit as st
import datetime
import json
import sqlite3
from streamlit_calendar import calendar
from markdowncss import *
from banco import *
import time
from markdowncss import *
import datetime
import io

def calendarpage():    
    
    toastmessage()  
    popovercalendarmarkdown()
        
    st.markdown('''<style>
                [data-testid="stAppViewBlockContainer"]{
                    margin-top: -5rem !important;
                }
                
                
                
                </style>''', unsafe_allow_html=True)
                  
    csscal = calendarcss()
    
    caloption = calendaroption()
    
    dadosmeeting = eventos()
    
    dadosrecurrentes = eventosrecorrentes()

    events = []
    
    for reuniao in dadosmeeting:
        
        
        title = f"Reunião sobre: {reuniao[3]}"
        
        
        
        
        start = f"{reuniao[2]}T{reuniao[6]}" #data e hora inicio
        
        end = f"{reuniao[2]}T{reuniao[7]}" #data e hora fim
        
        encerramento = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M")
        
        remoção = encerramento + datetime.timedelta(minutes=30)
        
        if datetime.datetime.now() >= remoção:
            
            with sqlite3.connect('database/meetingdatabase.db') as conn:
                
                try:
                    
                    cursor =  conn.cursor()
                    
            
                    cursor.execute("DELETE FROM meetingdatabase WHERE id = ?", (reuniao[0],))
                    
                    conn.commit()
                    
                    st.rerun()

                except sqlite3.Error as e:
                    
                    print("Erro ao remover reuniao:", e)

        else:
            st.markdown('''<style>
                        .fc-timegrid-event{
                            font-size: 60px;
                        }
                        
                        
                        </style>''',unsafe_allow_html=True)
            
            events.append(
                    
                    
                    {
                        "title": title,
                        "start": start,
                        "end": end,
                    }
                )
                
                
    for reunioes in dadosrecurrentes:
        
        title = f"Reunião sobre: {reunioes[3]}"
        
        start = f"{reunioes[2]}T{reunioes[6]}" #data e hora inicio
        
        end = f"{reunioes[2]}T{reunioes[7]}" #data e hora fim
        
        encerramento1 = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M")
        
        remoção1 = encerramento1 + datetime.timedelta(minutes=30)
        
        if datetime.datetime.now() >= remoção1:
            
            with sqlite3.connect('database/meetingdatabase.db') as conn:
                
                try:
                    
                    cursor =  conn.cursor()
                    
            
                    cursor.execute("DELETE FROM currentmeeting WHERE id = ?", (reuniao[0],))
                    
                    conn.commit()
                    
                    st.rerun()

                except sqlite3.Error as e:
                    
                    print("Erro ao remover reuniao:", e)

        else:
        
            events.append(
                    {
                        "title": title,
                        "start": start,
                        "end": end,
                    }
                )
    
    
    ass = calendar(events = events, options = caloption, custom_css = csscal)
    
    col1, col3 = st.columns(2)
    
    coluna = col1
    coluna3 = col3
    
    if st.session_state["filter"] == "Admin":
    
        popovercalendarmarkdown()
        with coluna:
            with st.popover("Agendar Reunião", use_container_width=True):

                reuniaorecorrente = st.checkbox("Agendar reunião recorrente")

                if reuniaorecorrente == True:
                    checkboxcalendar()


                colums = st.columns(2, gap="small")

                with colums[0]:
                
                    rooms =  getallrooms()

                    nomereuniao =  st.text_input("Nome da Reunião", placeholder="Insira o nome da reunião")

                    assunto = st.text_input("Assunto da reunião", placeholder="Insira o assunto da reunião")

                    data = st.date_input("Selecione a data da reunião",format="YYYY-MM-DD",value=datetime.date.today())

                    salas = st.multiselect("Selecione as salas existentes", rooms)



                    if reuniaorecorrente == True:

                        regra_recorrencia = st.selectbox('Selecione a regra de recorrência:', ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'])


                with colums[1]:

                    usuarios = getallusers()

                    horainicio = st.selectbox('selecione a hora',['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'],index=None)

                    horafim = st.selectbox("Selecione a hora de término",['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'],index=None)

                    selected_participants = st.multiselect("Selecione os participantes existentes", usuarios)

                    comentarios = st.text_input("Comentários",placeholder="Comentario sobre a reunião")


                    if reuniaorecorrente == True:


                        datafimrecorrencia = st.date_input('Data de término da recorrência:',format="YYYY-MM-DD",value=datetime.date.today())


                agendarbuttom = st.button("Agendar",key="agendar",use_container_width=True,disabled=False)

                if agendarbuttom and  reuniaorecorrente == False:

                        parcipantesteste = selected_participants

                        participantes = json.dumps(selected_participants)

                        roomsalas = json.dumps(salas)

                        horasinicio =  json.dumps(horainicio)

                        horainicioform = json.loads(horasinicio)

                        horasfim =  json.dumps(horafim) 

                        horasfimform = json.loads(horasfim)

                        participantes_sem_aspas = participantes.strip('[]').replace('"', '')

                        salas_sem_aspas = roomsalas.strip('[]').replace('"', '')


                        insertmeeting(assunto, data, nomereuniao, comentarios, horainicioform, horasfimform, participantes_sem_aspas, salas_sem_aspas)

                        st.success("Reunião agendada com sucesso!")
                        
                        time.sleep(1)

                        for parcipante in parcipantesteste:


                            emaildestinatario = enviar(parcipante)

                            alertadestinatario = enviar(parcipante)
            

                            if  alertadestinatario:

                                organizador = st.session_state.get('name')

                                data_formatada = data.strftime("%d/%m/%Y")


                                msg = "O organizador <span style='font-weight: bold; color: blue;'>{}</span> agendou uma reunião com você marcada para <span style='font-weight: bold;'>{}</span> a partir das <span style='font-weight: bold;'>{}</span> até as <span style='font-weight: bold;'>{}</span> na <span style='font-weight: bold;'>{}</span>".format(organizador,data_formatada,horainicioform,horasfimform,salas_sem_aspas)


                                insertalert(alertadestinatario,msg)

                                enviar_email(emaildestinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas, organizador)

                            else:

                                print("Endereço de e-mail não encontrado para o usuário:", parcipante)
                                
                        st.rerun()

                elif agendarbuttom and  reuniaorecorrente == True:

                        parcipantesteste = selected_participants

                        participantes = json.dumps(selected_participants)

                        roomsalas = json.dumps(salas)

                        horasinicio =  json.dumps(horainicio)

                        horainicioform = json.loads(horasinicio)

                        horasfim =  json.dumps(horafim) 

                        horasfimform = json.loads(horasfim)

                        participantes_sem_aspas = participantes.strip('[]').replace('"', '')

                        salas_sem_aspas = roomsalas.strip('[]').replace('"', '')

                        for parcipante in parcipantesteste:


                            emaildestinatario = enviar(parcipante)

                            alertadestinatario = enviar(parcipante)

                            if emaildestinatario and alertadestinatario:

                                organizador = st.session_state.get('name') 

                                data_formatada = data.strftime("%d/%m/%Y")


                                msg = "O organizador <span style='font-weight: bold; color: blue;'>{}</span> agendou uma reunião com você marcada para <span style='font-weight: bold;'>{}</span> a partir das <span style='font-weight: bold;'>{}</span> até as <span style='font-weight: bold;'>{}</span> na <span style='font-weight: bold;'>{}</span>".format(organizador,data_formatada,horainicioform,horasfimform,salas_sem_aspas)

                                insertalert(alertadestinatario, msg)

                                enviar_email(emaildestinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas,organizador)

                            else:

                                print("Endereço de e-mail não encontrado para o usuário:", parcipante)


                        insert_recurring_meetings(assunto, data, datafimrecorrencia, nomereuniao, comentarios, horainicioform, horasfimform, participantes_sem_aspas, salas_sem_aspas, regra_recorrencia)
    
        popovercalendarmarkdownleft()          
        with coluna3:

            with st.popover("Alterar/Excluir", use_container_width=True):
                col1, col3 = st.columns(2)

                coluna = col1
                coluna3 = col3

                with coluna.container(height=60, border=True):

                    alterar = st.checkbox("Alterar", key="alterar")    

                with coluna3.container(height=60, border=True):
                    excluir = st.checkbox("Excluir", key="excluir")



                meetings = get_all_meetings()
                meeting_options = [f"ID: {meeting['Id']} | Nome: {meeting['Nome']} | Participantes: {meeting['Participantes']}" for meeting in meetings]
                selected_meeting = st.selectbox("Selecione a reunião:", meeting_options, index=None, key="meeting")

                if alterar == True:

                    with coluna:
                        usuarios = getallusers()

                        horaalterarbase = st.selectbox('Selecione a hora', ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'], index=None, key="alterarbase")

                        horafimalterar = st.selectbox("Selecione a hora de término", ['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'], index=None, key="alterarhorafim")


                        altparticipantes = st.multiselect("Selecione os participantes existentes", usuarios, key="altparticipantes")

                    with coluna3:

                        dataALT = st.date_input("Selecione a data da reunião",format="YYYY-MM-DD", key="altdatas",value=None)

                        salasALT = st.multiselect("Selecione as salas existentes", rooms, key="altsalas")

                        motivo =  st.text_input("Motivo", key="motivo")



                agendarbuttom = st.button("Confirmar",key="Confirmar",use_container_width=True,disabled=False)

                if agendarbuttom and alterar == False and excluir == False:

                    st.warning("Selecione uma opção") 

                if agendarbuttom and alterar == True:

                    if selected_meeting:
                    

                        meeting_id = int(selected_meeting.split("ID: ")[1].split(" |")[0])
                        
                        nomereuniao = str(selected_meeting.split("Nome: ")[1].split(" |")[0])


                        data = dataALT
                        nomereuniaoalt = nomereuniao
                        horasinicioalt = horaalterarbase
                        horasfimalt = horafimalterar

                        horasinicioalt =  json.dumps(horasinicioalt)

                        horainicioformalt = json.loads(horasinicioalt)

                        horasfimlts =  json.dumps(horasfimalt) 

                        horasfimformalt = json.loads(horasfimlts)

                        participantes = json.dumps(altparticipantes)
                        participanteslatsemaspas = participantes.strip('[]').replace('"', '')

                        salas = json.dumps(salasALT)
                        salasaltsemaspas = salas.strip('[]').replace('"', '')

                        motivo = motivo



                        update_meeting(meeting_id, data, nomereuniao, horainicioformalt, horasfimformalt, participanteslatsemaspas, salasaltsemaspas, motivo)


                        st.success("Reunião atualizada com sucesso!")
                        
                        st.rerun()

                    else:

                        st.warning("Selecione uma reunião antes de confirmar a alteração.")

                if agendarbuttom and excluir == True:

                    if selected_meeting:

                        meeting_id = int(selected_meeting.split("ID: ")[1].split(" |")[0])
                        avisoparticipantes = selected_meeting.split("Participantes: ")[1].split(" |")[0].split(", ")
                        
                        
                        selected_meeting_data = get_meeting_data_by_id(meeting_id)
                        
                        for participante in avisoparticipantes:
                            
                            alertadestinatario = enviar(participante)
                            
                            if alertadestinatario:
                                
                                if selected_meeting_data:
                                    
                                    organizador = st.session_state.get('name')
                                    
                                    data_reuniaoexc = selected_meeting_data["Data"]
                                    
                                    hora_inicioexc = selected_meeting_data["HoraStart"]
                                    
                                    hora_fimexc = selected_meeting_data["HoraEnd"]
                                    
                                    salaexc = selected_meeting_data["Sala"]
                                
                                    
                                    formatdataexc =  datetime.datetime.strptime(data_reuniaoexc, '%Y-%m-%d').strftime('%d/%m/%Y')
                                
                        
                        
                                    msg = "O organizador <span style='font-weight: bold; color: blue;'>{}</span> cancelou a reunião marcada para <span style='font-weight: bold;'>{}</span> a partir das <span style='font-weight: bold;'>{}</span> até as <span style='font-weight: bold;'>{}</span> na <span style='font-weight: bold;'>{}</span>".format(organizador,formatdataexc,hora_inicioexc,hora_fimexc,salaexc)   
                               
                                    insertalert(alertadestinatario, msg)
                                    

                            else:
                                print(f"Erro ao enviar alerta para: {alertadestinatario}")

                       

                        delete_meeting(meeting_id)
                        
                        time.sleep(1)
                        
                        st.rerun()

                    else:

                        st.warning("Selecione uma reunião antes de confirmar a exclusão.")

    
    else:
        
        popovercalendarmarkdown()
        
        with st.popover("Agendar Reunião", use_container_width=True):
            
            reuniaorecorrente = st.checkbox("Agendar reunião recorrente")
            
            if reuniaorecorrente == True:
                
                checkboxcalendar()
                
            colums = st.columns(2, gap="small")
            
            with colums[0]:
            
                rooms =  getallrooms()
                
                nomereuniao =  st.text_input("Nome da Reunião", placeholder="Insira o nome da reunião")
                
                assunto = st.text_input("Assunto da reunião", placeholder="Insira o assunto da reunião")
                
                data = st.date_input("Selecione a data da reunião",format="YYYY-MM-DD",value=datetime.date.today())
                
                salas = st.multiselect("Selecione as salas existentes", rooms)
                
                if reuniaorecorrente == True:
                    
                    regra_recorrencia = st.selectbox('Selecione a regra de recorrência:', ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'])
                    
            with colums[1]:
                
                usuarios = getallusers()
                horainicio = st.selectbox('selecione a hora',['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'],index=None)
                
                horafim = st.selectbox("Selecione a hora de término",['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00'],index=None)
                
                selected_participants = st.multiselect("Selecione os participantes existentes", usuarios)
                
                comentarios = st.text_input("Comentários",placeholder="Comentario sobre a reunião")
                
                if reuniaorecorrente == True:
                    
                    datafimrecorrencia = st.date_input('Data de término da recorrência:',format="YYYY-MM-DD",value=datetime.date.today())
                    
            agendarbuttom = st.button("Agendar",key="agendar",use_container_width=True,disabled=False)
            
            if agendarbuttom and  reuniaorecorrente == False:
                
                    parcipantesteste = selected_participants
                    
                    participantes = json.dumps(selected_participants)
                    
                    roomsalas = json.dumps(salas)
                    
                    horasinicio =  json.dumps(horainicio)
                    
                    horainicioform = json.loads(horasinicio)
                    
                    horasfim =  json.dumps(horafim) 
                    
                    horasfimform = json.loads(horasfim)
                    
                    participantes_sem_aspas = participantes.strip('[]').replace('"', '')
                    
                    salas_sem_aspas = roomsalas.strip('[]').replace('"', '')
                    
                    insertmeeting(assunto, data, nomereuniao, comentarios, horainicioform, horasfimform, participantes_sem_aspas, salas_sem_aspas)
                    
                    st.success("Reunião agendada com sucesso!")
                    
                    for parcipante in parcipantesteste:
                        
                        emaildestinatario = enviar(parcipante)
                        
                        alertadestinatario = enviar(parcipante)
                        
                        if  alertadestinatario:
                            
                            organizador = st.session_state.get('name')
                            
                            data_formatada = data.strftime("%d/%m/%Y")
                            
                            msg = "O organizador <span style='font-weight: bold; color: blue;'>{}</span> agendou uma reunião com você marcada para <span style='font-weight: bold;'>{}</span> a partir das <span style='font-weight: bold;'>{}</span> até as <span style='font-weight: bold;'>{}</span> na <span style='font-weight: bold;'>{}</span>".format(organizador,data_formatada,horainicioform,horasfimform,salas_sem_aspas)
                            
                            insertalert(alertadestinatario,msg)
                            
                            enviar_email(emaildestinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas)
                            
                        else:
                            
                            print("Endereço de e-mail não encontrado para o usuário:", parcipante)
                            
            elif agendarbuttom and  reuniaorecorrente == True:
                
                    parcipantesteste = selected_participants
                    
                    participantes = json.dumps(selected_participants)
                    
                    roomsalas = json.dumps(salas)
                    
                    horasinicio =  json.dumps(horainicio)
                    
                    horainicioform = json.loads(horasinicio)
                    
                    horasfim =  json.dumps(horafim) 
                    
                    horasfimform = json.loads(horasfim)
                    
                    participantes_sem_aspas = participantes.strip('[]').replace('"', '')
                    
                    salas_sem_aspas = roomsalas.strip('[]').replace('"', '')
                    
                    for parcipante in parcipantesteste:
                        
                        emaildestinatario = enviar(parcipante)
                        
                        alertadestinatario = enviar(parcipante)
                        
                        if emaildestinatario and alertadestinatario:
                            
                            organizador = st.session_state.get('name') 
                            
                            data_formatada = data.strftime("%d/%m/%Y")
                            
                            msg = "O organizador <span style='font-weight: bold; color: blue;'>{}</span> agendou uma reunião com você marcada para <span style='font-weight: bold;'>{}</span> a partir das <span style='font-weight: bold;'>{}</span> até as <span style='font-weight: bold;'>{}</span> na <span style='font-weight: bold;'>{}</span>".format(organizador,data_formatada,horainicioform,horasfimform,salas_sem_aspas)
                            
                            insertalert(alertadestinatario, msg)
                            
                            enviar_email(emaildestinatario,nomereuniao,data,horainicioform,horasfimform,salas_sem_aspas, organizador=st.session_state.get('name'))
                            
                        else:
                            
                            print("Endereço de e-mail não encontrado para o usuário:", parcipante)
                            
                    insert_recurring_meetings(assunto, data, datafimrecorrencia, nomereuniao, comentarios, horainicioform, horasfimform, participantes_sem_aspas, salas_sem_aspas, regra_recorrencia)
               
    st.write(events)
    

def cadastropage():
    
        toastmessage()
        padraomargin()
        with st.container(height=300, border=True):
            
            
            
            container = st.container()
            container.title(":heavy_plus_sign: Cadastrar")
            container.caption('''
                        A área de cadastro conta com as seguintes opções:
                
                        ''')
            col1, col3 = st.columns(2)
            
            sucessone,sucesstwo = st.columns(2)
            
            colunasucess1 = sucessone
            colunasucess2 = sucesstwo
            

            coluna = col1
            
            coluna_2 = col3
            
            with coluna.container(height=40, border=False):
        
            
                with st.popover("Cadastro", use_container_width=True):
                    
                    popovermarkdown()
                    
                    st.markdown("Cadastrar Usuário 👋")
                    
                    
                    
                    username = st.text_input(label='Nome de Usuário', placeholder='Insira nome de usuário(email)')
                    email = ''
                    Permission = st.selectbox(label='Permissão', options=['Admin', 'User'], index=None, placeholder='Selecione o tipo de permissão')


                    if st.button('Confirmar', key='usersignup', type='primary'):
                        
                        if not username or not Permission:
                            
                            colunasucess2.warning('Por favor, preencha todos os campos')
                        
                        elif not validate(username):
                            
                            st.toast("Por favor, insira um email valido", icon="🆘")
                            
                        elif verify(username):
                            
                            st.toast("Por favor, insira um que não esteja em uso", icon="🆘")
                            
                        else:
                            
                            try:
                                inserir_usuario(username, email, Permission)
                                
                                container.success('Conta criada com sucesso!')
                                
                                st.toast('''A senha padrão para novos usuarios é
                                          123''', icon="⚠️")
                                
                                
                            except Exception as e:
                                
                                container.error('Erro ao criar conta: ' + str(e))
                            
            
            with coluna_2.container(height=60, border=False):
                
                with st.popover("Configurações", use_container_width=True):
                    
                    popovermarkdown()
                    
                    st.markdown("Cadastrar Sala 👋")
                    
                    Roomname = st.text_input(label='Nome da Sala', placeholder='Insira  o nome da sala')
                    
                    if st.button('Confirmar', key='Roomsignup', type='primary'):
                        
                        if not Roomname:    
                            
                            colunasucess1.warning('Por favor, preencha todos os campos')
                        
                        elif verifyroom(Roomname):
                            
                            st.toast("Por favor, insira um que não esteja em uso", icon="🆘")
                            
                        else:
                            
                            try:
                                
                                inserirsala(Roomname)
                                
                                container.success('Sala criada com sucesso!')
                                
                            except Exception as e:
                                
                                container.error('Erro ao criar sala: ' + str(e))    

            popoversucessmarkdown()   
            
            colunasucess1.container(height=1, border=False)
            
            colunasucess2.container(height=1, border=False)
            
        divider()
        
        if st.button("Voltar para o menu",key="Back",use_container_width=True):
                st.session_state.nav = None
                st.rerun() 

def userpage():
    
    padraomargin1()
    
    respostas = requestuser()
    
    for resposta in respostas:

       if len(resposta) >= 4:  
           
        email = resposta[0]      
        data = resposta[2] 
        remove_participant(email, data)
              
       else:
           
           print("A resposta não tem dados suficientes.")
           
    confirmacoes = confirmuser()
    
    for confirmacao in confirmacoes:

       if len(confirmacao) >= 3:  
           
        emailconf = confirmacao[0]      
        data = confirmacao[2] 
        
        participante = requestusername(emailconf)
        
        
        data_obj = datetime.datetime.strptime(data, "%Y-%m-%d")
    
        data_formatada = data_obj.strftime("%d-%m-%Y")
        
        msg = "O participante <span style='font-weight: bold; color: blue;'>{}</span> confirmou sua presença para a reunião marcada para <span style='font-weight: bold;'>{}</span>".format(participante,data_formatada    )
        
        insertalert(emailconf,msg)
        
        remove_response(emailconf, data)
              
       else:
           
           print("A resposta não tem dados suficientes.")
    
    with st.container(height=540,border=True):
        
        
    
        columns = st.columns(2)
        
        coluna_user = columns[0].container(height=400)
        
        coluna_user.title(":lock_with_ink_pen: Dados do usuario")
        
        
        username = st.session_state.get(default="username",key="username")
        
        if username:
            
            dados = databaseuser(username)
            
            
            coluna_user.write(f'''<div style='border: 1px solid #ccc; border-radius: 5px; padding: 10px; text-align: left;'>
                          <b>⏹️Username:</b><br><span style=' color: rgb(23, 1, 67); font-weight: bold;'>{dados['nameuser']}
                          </span></div>''', unsafe_allow_html=True)
            
            coluna_user.write(f'''<div style='border: 1px solid #ccc; border-radius: 5px;padding: 10px;text-align: left;'>
                          <b>⏹️Email:</b><br><span style='color: rgb(23, 1, 67);font-weight: bold;'>{dados['email']}
                          </span></div>''', unsafe_allow_html=True)
            
            coluna_user.write(f'''<div style='border: 1px solid #ccc; border-radius: 5px;padding: 10px;text-align: left'>
                          <b>⏹️Tipo:</b><br><span style='color: rgb(23, 1, 67);font-weight: bold; '>{dados['Permission']}
                          </span></div>''', unsafe_allow_html=True)
            
    
    
        coluna_update = columns[1].container(height=400)
        
        coluna_update.title("🔔 Alertas")
    
        with coluna_update:
            
                verificar_mensagens()
                verificar_lembretes()
                
                if st.button("Limpar mensagens", key="Clear", use_container_width=True):
            
                    alertclean(username)
        
        
        divider()
        
        if st.button("Voltar para o menu",key="Back",use_container_width=True):
                st.session_state.navmenu = None
                st.rerun()  
                
                
def updatepassword():
    
    padraomargin()
    
    with st.container( border=False):
        
        toastmessage()
        
        columns = st.columns(1)
        
        coluna1 = columns[0].container(height=330,border=True)
        
        coluna1.title("🔐 Redefinir")
        
        containerupdate = st.container()

        with coluna1.form('Redefinir', clear_on_submit=True, border=False):
            
            newpassword = st.text_input(label='Nova Senha',placeholder="Insira sua senha")
            
            confirmnewpassword = st.text_input(label='Confirme a Nova Senha', placeholder='Confirme a nova senha')

            if st.form_submit_button('Redefinir'):
                
                if len(newpassword) >= 8 and len(confirmnewpassword) >= 8:
                
                    if newpassword != "" and confirmnewpassword != "" and newpassword == confirmnewpassword:

                        username = st.session_state.username


                        if username:  

                            if resetpassword(username, newpassword):

                                containerupdate.success("Senha redefinida com sucesso!")

                            else:

                                st.toast("Erro ao redefinir a senha.", icon="❌")
                        else:

                            st.toast("Erro ao redefinir a senha.", icon="❌")

                    elif not newpassword or not confirmnewpassword:
                    
                        st.toast("As senhas devem ser preenchidas.", icon="🚨")
     
                    else:
                        
                        st.toast("As senhas inseridas não correspondem.", icon="❌")
                        
                else:
                    
                    st.toast("As senhas devem ter pelo menos 8 caracteres.", icon="🚨")
                    
                    
    divider()
                    
    if st.button("Voltar para o menu",key="Back",use_container_width=True):
                st.session_state.navmenu = None
                st.rerun()
                
def gerenciarpage():
    
    padraomargin()
    
    popovermarkdown()
    
    colum = st.columns(1)
    
    with colum[0].container(height=400, border=True):
    
        try:
        
            with sqlite3.connect('database/usersdatabase.db') as conn:
            
                usuarios = pd.read_sql_query("SELECT username, nameuser, Permission FROM usuarios", conn)

                if usuarios.empty:
                
                    st.write("Nenhum usuário cadastrado.")
                
                else:
                    # Renomear as colunas
                    usuarios = usuarios.rename(columns={'Permission': 'Privilegio','nameuser':'Nome','username':'Usuário'})
                    
                    st.markdown('''<style>
                                
                                [data-testid="stElementToolbar"]{
                                    
                                    display: none;
                                    cursor: pointer;}
                                
                                [data-testid="StyledLinkIconContainer"] {
                                    text-align: center;
                                    
                                }
                                
                                [data-testid="data-grid-canvas"] {
                                    text-align: center;
                                    background-color: #f0f0f0;
                                }
                                
                                </style>''', unsafe_allow_html=True)
                    
                    
                    st.subheader("Usuários Cadastrados:")
                    
                    st.dataframe(usuarios, hide_index=True, use_container_width=True)
                    
                    
                    
                    
                    with st.popover("Excluir Usuários", use_container_width=True):
                        
                            usuarios_selecionados = st.multiselect("Selecione os usuários para excluir:", usuarios['Usuário'])
                    
                            if st.button("Excluir Usuário", key="Delete", use_container_width=True):

                                with sqlite3.connect('database/usersdatabase.db') as conn:

                                    c = conn.cursor()

                                    for usuario in usuarios_selecionados:

                                        c.execute("DELETE FROM usuarios WHERE username = ?", (usuario,))

                                    conn.commit()

                                    st.success("Usuários excluídos com sucesso!")
                                    
                                    st.rerun()
                        
                
        except sqlite3.Error as e:
        
            print("Erro ao recuperar usuários:", e) 
        
    divider()

    if st.button("Voltar para o menu", key="Back",use_container_width=True):
        st.session_state.nav = None
        st.rerun() 
        
def relatoriopage():

        relatorios('meetingdatabase','currentmeeting')        
           
        st.markdown('''<style> 

                    [data-testid="baseButton-secondary"][class="st-emotion-cache-13ejsyy ef3psqc12"]{
                        
                    
                        width:74px!important;
                        height:28px!important;
                        padding: 4px 12px 4px 12px!important;
                       
                    }                
                    
                    [data-testid="element-container"][class="element-container st-emotion-cache-7veruy e1f1d6gn4"]{
                        
                        width: 287px!important;
                        height: 38px!important;
                    }
                    
                    [class="custom-divider"]{
                        
                        width: 287px!important;
                        height: 1px!important;
                    }
                    
                    
                    
                    [data-testid="stButton"][class="row-widget stButton"]{
                        margin-top: 40px!important;
                        font-size: 16px!important;
                    }

                    [data-testid="baseButton-secondary"][class="st-emotion-cache-13ejsyy ef3psqc12"]{
                        font-size: 59px!important;
                        
                    }
                    
                    
                    
                    </style>''', unsafe_allow_html=True)
        
        
        
        
        st.title("Relatórios")
        
        
        file_path = "database/relatorios.csv" 
        
        with open(file_path, "rb") as f:
            
          s = f.read()
 
        df=pd.read_csv(io.StringIO(s.decode('utf-8')))
 
        df['Data'] = pd.to_datetime(df['Data'])
        
        df['Data'] = pd.to_datetime(df['Data'], utc=True)

 
        def remote_css(url):
            
            
            
            st.markdown(f'<link href="{url}" rel="stylesheet">',
                        unsafe_allow_html=True)
            

 
        def header_bg(table_type):  
            if table_type == "BASE TABLE":
                return "tablebackground"
            elif table_type == "VIEW":
                return "viewbackground"
            else:
                return "mvbackground"
            
        def local_css():
            with open("styles/relatorio.css") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                    
        remote_css(
            "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")
        
        local_css()

 
        selectbox_orderby = st.selectbox(index=0, label="Ordenar por:", options= ('Data de criação ↓ (Mais antigas)', 'Data de criação ↑ (Mais recentes)'))
        
        
 
 
        orderby_column = ''
        orderby_asc = True
 
 
        if selectbox_orderby == 'Data de criação ↓ (Mais antigas)':
            orderby_column = 'Data'
            orderby_asc = False
        elif selectbox_orderby == 'Data de criação ↑ (Mais recentes)':
            orderby_column = 'Data'
            orderby_asc = True
 
 
        df.sort_values(by=[orderby_column], inplace=True, ascending=orderby_asc) 
 
        table_scorecard = """
        <div class="ui one small statistics">
          <div class="grey statistic">
            <div class="grey label">
            Tabelas
                        </div>
          </div>
        </div>"""
        
        table_scorecard += """<br><br><br><div id="mydiv" class="ui centered cards">"""
        
        for index, row in df.iterrows():
            table_scorecard += """
        <div class="card">  
            <div class=" content """"""">
                    <div class=" header smallheader">"""+str(row['NomeReuniao'])+"""</div>
            <div class="meta smallheader">Assunto:"""+str(row['Assunto'])+"""</div>
            </div>
            <div class="content">
                <div class="description"><br>
                        <p class="kpi text">Participantes:</b>
                        <div class="user icon">"""+"{0:}".format(row['Participantes'])+"""<br>
                    </div>
                </div>
            </div>
            <div class="extra content">
                <div class="meta"><i class="user icon"></i> Organizador: """+str(row['Organizador'])+""" </div>
                <div class="meta"><i class="calendar alternate outline icon"></i> Criado Em: """+str(row['Data'].strftime("%d/%m/%Y"))+"""</div>
                <div class="meta"><i class="history icon"></i> Horario """+str(row['HoraEnd']).strip("")+"""</div>
                <div class="meta"><i class="edit icon"></i> Última Alteração: """+str(row['Data'].strftime("%d/%m/%Y"))+"""</div>
                <div class="meta"><i class="comment alternate outline icon"></i> Comentário: """+str(row['Comentarios'])+""" </div>
            </div>
        </div>"""
        
        st.markdown(table_scorecard, unsafe_allow_html=True)