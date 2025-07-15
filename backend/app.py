from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os

from utils.responder import retrieve_top_chunks, generate_response, stream_response

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query is required."}), 400

    index_path = "data/index.faiss"
    meta_path = "data/metadata.json"

    try:
        top_chunks = retrieve_top_chunks(query, index_path, meta_path)
        if not top_chunks:
            return jsonify({"error": "No relevant data found."}), 404

        answer = generate_response(query, top_chunks)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stream', methods=['POST'])
def stream():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query is required"}), 400

    index_path = "data/index.faiss"
    meta_path = "data/metadata.json"

    try:
        chunks = retrieve_top_chunks(query, index_path, meta_path)
        if not chunks:
            return jsonify({"error": "No relevant data found"}), 404

        def generate():
            for word in stream_response(query, chunks):
                yield word

        return Response(generate(), content_type='text/plain')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


    
