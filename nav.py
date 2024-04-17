import streamlit as st
from pages import *


def menucadastro():
    
    
    nav = st.session_state.get('nav', None)
    
    if nav is None:
            columns = st.columns(2)
            
            coluna1 = columns[0].container(height=320)
            
            coluna1.title(":heavy_plus_sign: Cadastrar")
            
            coluna1.write('''Você será redirecionado para nossa página de cadastro de usuários.
                          Lá, você poderá preencher os dados necessários para criar uma nova conta\n''')
            
            
            coluna2 = columns[1].container(height=320)
            
            coluna2.title(":spiral_note_pad: Gerenciar")
            
            coluna2.write('''Você será redirecionado para nossa página de gerenciamento de usuários.
                          Lá, você poderá gerenciar as contas de usuários\n''')

            navcadastro = coluna1.button("Cadastrar")
            navgerenciar = coluna2.button("Gerenciar")

            if navcadastro:
                nav = 'Cadastrar'
                st.session_state.nav = nav
                st.rerun()
            elif navgerenciar:
                nav = 'Gerenciar'
                st.session_state.nav = nav
                st.rerun()

    else:
            if nav == 'Cadastrar':
                cadastropage()
            
            if nav == 'Gerenciar':
                gerenciarpage()



def menuconfig():
    
    nav = st.session_state.get('navmenu', None)

    if nav is None:
            
        with st.container(height=360, border=False):    
            columns = st.columns(2)
            
            coluna1 = columns[0].container(height=320)
            
            coluna1.title(":key: Redefinir Senha")
            
            coluna1.write('''Você será redirecionado para nossa página de redefinir a senha''')
            
            coluna2 = columns[1].container(height=320)
            
            coluna2.title(":lock_with_ink_pen: Dados do usuario")

            navalterar = coluna1.button("Alterar")
            navvisualizar = coluna2.button("Visualizar")

            if navalterar:
                nav = 'Alterar'
                st.session_state.navmenu = nav
                st.rerun()
            elif navvisualizar:
                nav = 'Visualizar'
                st.session_state.navmenu = nav
                st.rerun()
    else:
            if nav == 'Visualizar':
                userpage()
            
            elif nav == 'Alterar':
                updatepassword()