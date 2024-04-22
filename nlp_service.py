# nlp_service.py
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = 'your_openai_api_key'

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "user", "content": text}
        ]
    )
    sql_query = response.choices[0].message['content']
    return jsonify({'sql_query': sql_query})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
