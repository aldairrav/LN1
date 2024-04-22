# user_interface_service.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message_received():
    message = request.json.get('message')
    # Enviar mensaje al servicio de NLP y esperar la consulta SQL
    response = requests.post('http://nlp_service:5001/translate', json={'text': message})
    sql_query = response.json().get('sql_query')
    
    # Enviar consulta SQL al servicio de Base de Datos y obtener resultados
    db_response = requests.post('http://database_service:5002/execute', json={'query': sql_query})
    results = db_response.json().get('results')
    
    return jsonify({'response': results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
