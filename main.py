from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Simulated database for drug information
drug_database = {}

@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <html>
        <head>
            <title>Drug Information API</title>
            <style>
                body {
                    background-color: black;
                    color: orange;
                    font-family: Arial, sans-serif;
                }
                .container {
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #222;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                }
                h1 {
                    text-align: center;
                    color: #FFA500;
                }
                p {
                    text-align: center;
                    margin-bottom: 30px;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                input[type="text"] {
                    width: 80%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #FFA500;
                    border-radius: 5px;
                    background-color: #333;
                    color: white;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    background-color: #FFA500;
                    color: black;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #ffb732;
                }
                .result {
                    margin-top: 20px;
                    word-wrap: break-word;
                    white-space: pre-wrap;
                }
                .drug-info, .side-effects {
                    margin-bottom: 20px;
                }
                .drug-info h2, .side-effects h2 {
                    color: #FFA500;
                }
                .drug-info p, .side-effects p {
                    background-color: #333;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-wrap: break-word;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Drug Information API</h1>
                <p>Enter drug names separated by commas:</p>
                <form action="/drugs" method="post">
                    <input type="text" name="drug_names" placeholder="aspirin, ibuprofen, paracetamol">
                    <input type="submit" value="Get Drug Information">
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/drugs', methods=['GET', 'POST'])
def get_drug_info():
    try:
        if request.method == 'POST':
            if request.form.get('drug_names'):
                drug_names = request.form.get('drug_names').split(',')
            else:
                drug_names = request.json.get('drug_names', [])
            if not drug_names:
                return jsonify({"error": "No drug names provided"}), 400

        all_drug_info = []
        all_side_effects = set()
        
        for drug_name in drug_names:
            drug_name = drug_name.strip()
            if drug_name in drug_database:
                info = drug_database[drug_name]
            else:
                response = requests.get(f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}")
                if response.status_code == 200:
                    drug_data = response.json()
                    if 'results' in drug_data and drug_data['results']:
                        item = drug_data['results'][0]
                        info = {
                            "official_name": item.get("openfda", {}).get("brand_name", ["N/A"])[0],
                            "generic_name": item.get("openfda", {}).get("generic_name", ["N/A"])[0],
                            "safe_usage": item.get("indications_and_usage", "N/A"),
                            "dosage_form": item.get("openfda", {}).get("dosage_form", ["N/A"])[0],
                            "route": item.get("openfda", {}).get("route", ["N/A"])[0],
                            "substance_name": item.get("openfda", {}).get("substance_name", ["N/A"])[0],
                            "side_effects": item.get("adverse_reactions", "N/A")
                        }
                        drug_database[drug_name] = info
                        if "adverse_reactions" in item:
                            side_effects = item["adverse_reactions"]
                            all_side_effects.update(side_effects.split('\n'))
                    else:
                        info = {"error": "Drug not found"}
                else:
                    info = {"error": "Failed to fetch drug information"}
            all_drug_info.append({drug_name: info})
        
        return render_template_string('''
            <!doctype html>
            <html>
            <head>
                <title>Drug Information Results</title>
                <style>
                    body {
                        background-color: black;
                        color: orange;
                        font-family: Arial, sans-serif;
                    }
                    .container {
                        max-width: 800px;
                        margin: 50px auto;
                        padding: 20px;
                        background-color: #222;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                    }
                    h1 {
                        text-align: center;
                        color: #FFA500;
                    }
                    .result {
                        margin-top: 20px;
                        word-wrap: break-word;
                        white-space: pre-wrap;
                    }
                    .drug-info, .side-effects {
                        margin-bottom: 20px;
                    }
                    .drug-info h2, .side-effects h2 {
                        color: #FFA500;
                    }
                    .drug-info p, .side-effects p {
                        background-color: #333;
                        padding: 10px;
                        border-radius: 5px;
                        overflow-wrap: break-word;
                        white-space: pre-wrap;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Drug Information Results</h1>
                    <div class="result">
                        <div class="drug-info">
                            <h2>Drug Information</h2>
                            {% for drug in drug_info %}
                                {% for name, info in drug.items() %}
                                    <p><strong>{{ name }}</strong></p>
                                    <p>Official Name: {{ info.official_name }}</p>
                                    <p>Generic Name: {{ info.generic_name }}</p>
                                    <p>Safe Usage: {{ info.safe_usage }}</p>
                                    <p>Dosage Form: {{ info.dosage_form }}</p>
                                    <p>Route: {{ info.route }}</p>
                                    <p>Substance Name: {{ info.substance_name }}</p>
                                    <p>Side Effects: {{ info.side_effects }}</p>
                                {% endfor %}
                            {% endfor %}
                        </div>
                        <div class="side-effects">
                            <h2>Potential Side Effects</h2>
                            {% if side_effects %}
                                <ul>
                                    {% for effect in side_effects %}
                                        <li>{{ effect }}</li>
                                    {% endfor %}
                                </ul>
                            {% else %}
                                <p>None</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </body>
            </html>
        ''', drug_info=all_drug_info, side_effects=list(all_side_effects))
        
    except Exception as err:
        app.logger.error('Error occurred: %s', err)
        return jsonify({"error": f"An error occurred: {err}"}), 500

@app.route('/drugs', methods=['PUT'])
def update_drug_info():
    try:
        data = request.json
        drug_name = data.get('drug_name')
        updated_info = data.get('updated_info')
        
        if not drug_name or not updated_info:
            return jsonify({"error": "drug_name and updated_info are required"}), 400
        
        drug_name = drug_name.strip()
        
        if drug_name not in drug_database:
            return jsonify({"error": "Drug not found in database"}), 404
        
        drug_database[drug_name].update(updated_info)
        
        return jsonify({"message": f"Drug information for {drug_name} updated successfully", "updated_info": drug_database[drug_name]})
    
    except Exception as err:
        app.logger.error('Error occurred: %s', err)
        return jsonify({"error": f"An error occurred: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
