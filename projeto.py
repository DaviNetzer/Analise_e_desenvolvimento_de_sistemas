# Sistema de Gestão de Tarefas - Iteração 1
# Stack sugerida: Flask (back-end), SQLite (banco leve embutido)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
db = SQLAlchemy(app)

# Modelo de Tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(500))
    prazo = db.Column(db.String(20))
    status = db.Column(db.String(20), default="pendente")

# Inicializar banco (executar uma vez no terminal)
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return "Sistema de Gestão de Tarefas rodando!"

# Criar tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    nova = Tarefa(
        titulo=dados['titulo'],
        descricao=dados.get('descricao', ''),
        prazo=dados.get('prazo', '')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa criada com sucesso!'}), 201

# Listar tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([
        {'id': t.id, 'titulo': t.titulo, 'descricao': t.descricao, 'prazo': t.prazo, 'status': t.status}
        for t in tarefas
    ])

# Editar tarefa
@app.route('/tarefas/<int:id>', methods=['PUT'])
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.prazo = dados.get('prazo', tarefa.prazo)
    tarefa.status = dados.get('status', tarefa.status)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa atualizada com sucesso!'})

# Excluir tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def excluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa excluída com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
