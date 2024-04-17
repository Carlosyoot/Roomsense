import streamlit as st

#markdown cached


def popovermarkdown():
    st.markdown('''
                                <style>
                                    [data-testid="stPopoverBody"]{
                                        margin-top: -50px;
                                    }
                                
                                
                                
                                
                                </style>''',unsafe_allow_html=True)
    
def popoversucessmarkdown():
    st.markdown('''
                        <style>
                            [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-76oqxp e1f1d6gn0"]{
                                margin-top: -50px;
                            }
                        
                        </style>
                        ''',unsafe_allow_html=True) 
    
def popovercalendarmarkdown():
    st.markdown('''
        <style>
            @media screen and (max-width: 1441px) {
                [data-testid="stPopoverBody"] {
                    margin-top: 120px !important;
                    height: 70vh !important;
                    width: 110vh !important;
                    margin-left: 11.5rem !important;
                }
            }
            @media screen and (min-width: 1440px) {
                [data-testid="stPopoverBody"] {
                    margin-top: -50px !important;
                    height: 50vh !important;
                    width: 70vh !important;
                    margin-left: 11.5rem !important;
                }
            }
        </style>
        ''', unsafe_allow_html=True)
    
def popovercalendarmarkdownleft():
    st.markdown('''
        <style>
            @media screen and (max-width: 1441px) {
                [data-testid="stPopoverBody"]{
                    margin-top: 120px !important;
                    height: 90vh !important;
                    width: 110vh !important;
                    margin-right: 11.5rem!important;
                }
            }
            @media screen and (min-width: 1440px) {
                [data-testid="stPopoverBody"] {
                    margin-top: -50px !important;
                    height: 60vh !important;
                    width: 70vh !important;
                    margin-right: 29.5rem !important;
                }
            }
        </style>
        ''', unsafe_allow_html=True)
    
    
    
def checkboxcalendar():
    st.markdown('''
                        <style>
                            @media screen and (max-width: 1441px) {
                                
                            
                            [data-testid="stPopoverBody"]{
                                margin-top: 120px;
                                height: 80vh;!important;
                                width: 110vh;!important;
                            }}
                            
                             @media screen and (min-width: 1440px) {
                                
                            
                            [data-testid="stPopoverBody"]{
                                margin-top: -50px;
                                height: 80vh;!important;
                                width: 110vh;!important;
                            }}
                        
                        </style>
                        ''',unsafe_allow_html=True)
    

@st.cache_data(show_spinner=True)
def divider():
    st.markdown('''
                            <style>
                            .scope .custom-divider {
                                background-image: linear-gradient(to right, rgb(255, 0, 0),rgb(114, 37, 208), rgb(47, 212, 42));
                                background-position: center;
                                background-repeat: no-repeat;
                                background-size: 100% 3px;
                                height: 2px;
                                margin-top: -0.1rem;
                            }
                            </style>

                            <div class="scope">
                                <hr class='custom-divider'>
                            </div>
                        ''', unsafe_allow_html=True)

@st.cache_data(show_spinner=True)
def custom_css():
            height = 600 
            st.markdown(f"""
                <style>
                    /* Definindo a altura padrão do container */
                    [data-testid="stVerticalBlockBorderWrapper"] {{
                        height: {height}px !important;
                    }}

                    /* Aplicando a regra de mídia para telas com largura máxima de 1441px */
                    @media screen and (max-width: 1441px) {{
                        [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-r421ms e1f1d6gn0"] {{
                            height: 320px !important; /* Defina a altura desejada para esta largura de tela */
                        }}
                    }}
                </style>
            """, unsafe_allow_html=True)

def toastmessage():
    st.markdown('''
                        <style>
                        
                            [data-testid="stToast"]{
                                font-size: 15px;
                                margin-button: 20px;
                                height: 100px;
                                border-radius: 35px;
                                text-align: center;
                                top: 70px;
                                position: fixed;
                                
                                
                                p {
                                font-size: 16px;
                                
                            }
                                
                            }
                            
                            
                        </style>
                        ''',unsafe_allow_html=True)
    
def padraomargin():
    st.markdown('''
                        <style>
                            @media screen and (max-width: 1441px) {
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-fmxa6b e1f1d6gn0"]{
                                    margin-top: -100px;
                                }
                            }

                            @media screen and (max-width: 1441px) {
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-g7r313 e1f1d6gn0"]{
                                    margin-top: -100px;
                                    
                                }
                                
                            }
                            
                            @media screen and (max-width: 1441px) {
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-1hrd9ol e1f1d6gn0"]{
                                    margin-top: -100px;
                                }
                                
                            }
                            
                            @media screen and (max-width: 1441px){
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-g7r313 e1f1d6gn0"]{
                                    margin-top: -100px;
                                }
                                
                            }
                            
                            
                            
                            
                        </style>
                        ''',unsafe_allow_html=True)
    
def padraomargin1():
    st.markdown('''<style>
                 @media screen and (max-width: 1441px) {
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-1qk1vby e1f1d6gn0"]{
                                    margin-top: -100px;
                                    border-color: white;

                                    
                                }
                                
                            }
                            
                 @media screen and (min-width: 1440px) {
                                [data-testid="stVerticalBlockBorderWrapper"][class="st-emotion-cache-1qk1vby e1f1d6gn0"]{
             
                                    border-color: white;

                                    
                                }
                                
                            }
                            </style>''',unsafe_allow_html=True)
    
def calendaroption():
    
    calendar_options = {
        
    "locale": "pt-br",
    "slotMinTime": "08:00:00",
    "slotMaxTime": "21:00:00",
    "initialView": "dayGridMonth",
    "nowIndicator": "true",
    "eventResizableFromStart": "true",
    
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "Week,dayGridMonth",
    },
    
    "views": {
                
            "Week": {
                "type": "timeGrid",
                "duration": {"days": 7},
                "hiddenDays": [0, 6],
                "allDaySlot": False
                
            },
            
            "dayGridMonth": {
                "fixedWeekCount": False  # Adicionando esta linha
            }
        }
    }
    
    return calendar_options


def calendarcss():
    
    custom_css = """
        fc-bg-event {
            background-color: red !important;
        }
    
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 500;
        }
        .fc-toolbar-title {
            font-size: 25px;
            color: blue;
        }
        .fc-timegrid-event{
                            font-size: 13px;
                            font-color: black!important;
                        }
        
    """
    
    return custom_css