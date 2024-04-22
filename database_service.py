# database_service.py
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="mrpan",
        user="postgres",
        password="postgres",
        port="5433"
    )
    return conn

@app.route('/execute', methods=['POST'])
def execute():
    query = request.json.get('query')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'results': results})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
