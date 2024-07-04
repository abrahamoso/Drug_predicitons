from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Drug Information API. Use /drugs/<drug_name> to get information about a specific drug."})

@app.route('/drugs', methods=['GET'])
def get_drug_info():
    return jsonify({"message": "Fetching drug information"})

@app.route('/drugs/<drug_name>', methods=['GET'])
def fetch_drug_info(drug_name):
    try:
        response = requests.get(f"https://api.fda.gov/drug/label.json?search=generic_name:{drug_name}")
        response.raise_for_status()  # Raise an error for bad status codes
        drug_data = response.json()
        
        if 'results' in drug_data:
            return jsonify(drug_data['results'])
        else:
            return jsonify({"error": "Drug not found"}), 404
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500
    except Exception as err:
        return jsonify({"error": f"Other error occurred: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
