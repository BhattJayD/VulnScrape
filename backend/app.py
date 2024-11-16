from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/cves', methods=['GET'])
def get_cves():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    return jsonify({"query":query})

if __name__ == '__main__':
    app.run(debug=True)
