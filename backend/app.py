from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/cves', methods=['GET'])
def get_cves():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    return jsonify({"query":query})

if __name__ == '__main__':
    app.run(debug=True)
