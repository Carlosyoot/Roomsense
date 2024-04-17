from flask import Flask
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
    app.run()
    
    
    
