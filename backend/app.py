from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.scraper import scrape_cves

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/cves', methods=['GET'])
def get_cves():
    # Get the 'query' parameter from the request
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Process the query with the scraper function
    try:
        cve_data = scrape_cves(query)
        return jsonify(cve_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
