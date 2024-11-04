from flask import Flask, jsonify, request
import pyodbc
#from sqlalchemy import false

app = Flask(__name__)


# Função de conexão com o SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=cepbr_exemplo.mssql.somee.com;'
        'DATABASE=cepbr_exemplo;'
        'UID=elamargo_SQLLogin_2;'
        'PWD=n81dzrtwf7'
    )
    return conn


# Rota da API para buscar dados de transportadora
@app.route('/api/', methods=['GET'])
def get_cidade():
    id_cidade = request.args.get('id')

    if not id_cidade:
        return jsonify({"error": "O parâmetro 'id' é necessário"}), 400

    # Converte o parâmetro para int, garantindo que seja um número
    try:
        id_cidade = int(id_cidade)
    except ValueError:
        return jsonify({"error": "O parâmetro 'id' deve ser um número inteiro"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta SQL para selecionar dados com base no ID_TRANSP
    query = '''
        SELECT id_cidade, cidade, uf, cod_ibge
        FROM cepbr_cidade
        WHERE id_cidade = ?
    '''
    cursor.execute(query, (id_cidade,))
    row = cursor.fetchone()

    # Processamento do resultado para JSON
    if row:
        cidade_data = {
            "ID_CIDADE": row[0],
            "CIDADE": row[1],
            "UF": row[2],
            "COD_IBGE": row[3]
        }
    else:
        # Retorna erro 404 se o registro não for encontrado
        return jsonify({"error": "Registro não encontrado"}), 404

    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    conn.close()

    return jsonify(cidade_data)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=False,host='0.0.0.0')
