import yaml;import streamlit as st;import streamlit_authenticator as stauth;import subprocess
from yaml import SafeLoader
from streamlit_option_menu import option_menu
from nav import *
from markdowncss import *
from banco import tip

if 'logout' not in st.session_state:
    
        st.session_state['logout'] = None

if st.session_state['logout'] == 'True':
    st.cache_data.clear()
    st.cache_resource.clear()

    st.session_state['logout'] = 'None'
    


def yamlconfig():        
    with open('config.yaml', 'r') as file:
        try:
             config = yaml.load(file, Loader=SafeLoader)
             return config
        except yaml.YAMLError as e:
            print("Yamlconfig(): " + str(e))
            
@st.cache_resource(experimental_allow_widgets=True,show_spinner=False)
def auth():
        authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookies']['name'],
        config['cookies']['key'],
        config['cookies']['expiry_days'],)   
        
        return authenticator
    
#    
#@st.cache_data(show_spinner=True)
#def start_flask_app():
#    flask_script_path = "mailer/teste.py"
#    print('iniciando flask')
#    subprocess.Popen(["python", flask_script_path])
    
@st.cache_data(show_spinner=True)
def custom_css():
            height = 600 
            st.markdown(f"""
                <style>
                    /* Definindo a altura padrão do container */
                    
                    @media screen and (min-width: 1440px){{
                    [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-r421ms e1f1d6gn0"]{{
                        height: {height}px !important;
                    }}
                    }}

                    /* Aplicando a regra de mídia para telas com largura máxima de 1441px */
                    @media screen and (max-width: 1441px) {{
                        [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-r421ms e1f1d6gn0"] {{
                            height: 320px !important; /* Defina a altura desejada para esta largura de tela */
                        }}
                    }}
                </style>
            """, unsafe_allow_html=True)
            

st.set_page_config(
    page_title="RoomSense - Home",
    page_icon=":calendar:",
    initial_sidebar_state="expanded")


from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)



def get_db_connection():
    
    conn = sqlite3.connect('mailer/respostas.db')
    
    conn.row_factory = sqlite3.Row
    
    return conn


@app.route('/confirmacaoA/<string:email>/<string:resposta>/<string:data>', methods=['GET'])
def confirmacao(email, resposta,data):
    
    inserir_resposta_no_banco(email, resposta,data)
    
    return render_template('index.html')


@app.route('/confirmacaoB/<string:email>/<string:resposta>/<string:data>', methods=['GET'])
def confirmacaob(email, resposta,data):
    
    inserir_resposta_no_banco(email, resposta,data)
        
    return render_template('index2.html')


def inserir_resposta_no_banco(email, resposta,data):
    
    conn = get_db_connection()
    
    conn.execute("INSERT INTO respostas (email, resposta,data) VALUES (?,?,?)", (email, resposta,data))
    
    conn.commit()
    
    conn.close()
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
            
    
config = yamlconfig()

authenticator = auth()

if 'authentication_status' not in st.session_state:
    
        st.session_state['authentication_status'] = None
        
if 'failed_login_attempts' not in st.session_state:
    
        st.session_state['failed_login_attempts'] = {}
        
        
if 'logout' not in st.session_state:
    
        st.session_state['logout'] = None

if 'name' not in st.session_state:
    st.session_state['name'] = None


authenticator.login() 

if st.session_state['authentication_status'] :
    
        menuoption = ['Home', 'Configurações', 'Relatorios']
    
        if 'filter' not in st.session_state:
            
            st.session_state['filter'] = tip()
            
        elif st.session_state['filter'] == 'Admin':
            
            menuoption.append('Cadastro')
            
            
            
        
            
        custom_css()
        
        with st.sidebar:
            
            
            st.markdown('''<style>
                                    [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-r421ms e1f1d6gn0"]{
                                        border-color: transparent;
                                        
                        
                        
                        </style>''',unsafe_allow_html=True)
            with st.container(border=True):
                
                
                
                
                menu_styles = {
                        "nav-link": {
                            "background-color": "white",
                            "color": "black",
                            "border-radius": "20px",
                            "padding": "5px 10px"
                        },
                        "nav-link-selected": {
                            "background-color": "blue",
                            "color": "white",
                            "border-radius": "20px",
                            "padding": "5px 10px"
                        }
                    }
                st.markdown('''
                                <style>
                                [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                                    overflow: hidden;
                                }
                                </style>
                            ''', unsafe_allow_html=True)


                selected = option_menu("Início", menuoption, 
                                        icons=['house', 'gear', 'list task', 'plus square'], 
                                        menu_icon="cast", 
                                        default_index=0, styles=menu_styles)

            
            
        
            divider()
            
            
            
            
            if st.session_state.get("name", "Usuário") is None:
                namelogged = "Usuário novo"
                
                
            else:
                namelogged = st.session_state["name"]
                
                
            st.write(f'''<span style="color: gray; font-size: 13px;;">Logado como: 
                     <span class="span" style="font-size: 18px; 
                     background-image: linear-gradient(to right, rgb(2, 97, 114), rgb(114, 37, 208), rgb(6, 2, 112)); 
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                     {namelogged}</span></div>''', unsafe_allow_html=True)

            authenticator.logout('Logout', 'sidebar')
               
            

            st.write(f'<span style ="color: rgb(186,185,185);font-size: 14px;">Versão 0.4.132</span>', unsafe_allow_html=True)


        #seleção de pagina

        if selected == 'Home':
            calendarpage()
        elif selected == 'Configurações':
            menuconfig()
        elif selected == 'Relatorios':
            relatoriopage()
        elif selected == 'Cadastro':
            menucadastro()


elif st.session_state['authentication_status'] is False:
    st.toast("Nome de usuário ou senha inválidos,", icon="🆘")
elif st.session_state['authentication_status'] is None:
    st.warning("Por favor, faca o login.", icon="🚨")