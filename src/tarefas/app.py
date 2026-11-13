from flask import Flask, render_template, request, redirect, url_for
from tarefas.models.database import Database

app = Flask(__name__)

def apagar_id_especificado(id):
    """
    Apaga uma tarefa específica do banco de dados MySQL com base no ID fornecido.
    """
    with Database() as db:
        # Corrigido para 'id_tarefa' para bater com o SELECT e com a sua tabela
        sql = "DELETE FROM tarefa WHERE id_tarefa = %s;"
        db.executar(sql, (id,))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        titulo = request.form.get('tituloTarefa')
        data = request.form.get('dataConclusao')
        
        if titulo:
            with Database() as db:
                sql = "INSERT INTO tarefa (titulo_tarefa, data_conclusao) VALUES (%s, %s);"
                db.executar(sql, (titulo, data if data else None))
                
        return redirect(url_for('home'))

    # Busca todas as tarefas cadastradas no banco de dados
    tarefas_da_pagina = []
    with Database() as db:
        resultado = db.executar("SELECT id_tarefa, titulo_tarefa, data_conclusao FROM tarefa;")
        if resultado:
            tarefas_da_pagina = resultado

    return render_template(
        'base.html',
        titulo='Lista de Tarefas do Theo',
        tarefas_da_pagina=tarefas_da_pagina
    )

@app.route('/apagar/<int:id>')
def apagar_tarefa(id):
    apagar_id_especificado(id)
    return redirect(url_for('home'))
    

if __name__ == '__main__':
    app.run(debug=True)