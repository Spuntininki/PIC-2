from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários
    return conn

# Inicializa o banco de dados
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Inquilinos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inquilino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        contato TEXT NOT NULL,
        enderecoImovel TEXT NOT NULL
    )
    ''')
    
    # Tabela de Aluguéis
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Aluguel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inquilino_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        dataVencimento TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (inquilino_id) REFERENCES Inquilino (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Rota para inicializar o banco de dados (para desenvolvimento)
@app.route('/init-db', methods=['GET'])
def initialize_database():
    init_db()
    return jsonify({'message': 'Database initialized successfully'})

# CRUD para Inquilinos
@app.route('/inquilinos', methods=['POST'])
def create_inquilino():
    data = request.get_json()
    nome = data.get('nome')
    contato = data.get('contato')
    enderecoImovel = data.get('enderecoImovel')
    
    if not (nome and contato and enderecoImovel):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Inquilino (nome, contato, enderecoImovel) VALUES (?, ?, ?)',
                   (nome, contato, enderecoImovel))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Inquilino criado com sucesso!'}), 201

@app.route('/inquilinos', methods=['GET'])
def get_inquilinos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Inquilino')
    inquilinos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(inquilinos)

@app.route('/inquilinos/<int:id>', methods=['PUT'])
def update_inquilino(id):
    data = request.get_json()
    nome = data.get('nome')
    contato = data.get('contato')
    enderecoImovel = data.get('enderecoImovel')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE Inquilino SET nome = ?, contato = ?, enderecoImovel = ? WHERE id = ?
    ''', (nome, contato, enderecoImovel, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Inquilino atualizado com sucesso!'})

@app.route('/inquilinos/<int:id>', methods=['DELETE'])
def delete_inquilino(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Inquilino WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Inquilino excluído com sucesso!'})

# CRUD para Aluguéis
@app.route('/aluguels', methods=['POST'])
def create_aluguel():
    data = request.get_json()
    inquilino_id = data.get('inquilino_id')
    valor = data.get('valor')
    dataVencimento = data.get('dataVencimento')
    status = data.get('status')
    
    if not (inquilino_id and valor and dataVencimento and status):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Aluguel (inquilino_id, valor, dataVencimento, status) VALUES (?, ?, ?, ?)
    ''', (inquilino_id, valor, dataVencimento, status))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Aluguel registrado com sucesso!'}), 201

@app.route('/aluguels', methods=['GET'])
def get_aluguels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Aluguel')
    aluguels = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(aluguels)

@app.route('/aluguels/<int:id>', methods=['PUT'])
def update_aluguel(id):
    data = request.get_json()
    status = data.get('status')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE Aluguel SET status = ? WHERE id = ?
    ''', (status, id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Status do aluguel atualizado com sucesso!'})

@app.route('/')
def serve_front():
    return send_from_directory(STATIC_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
