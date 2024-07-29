from flask import Flask, request, jsonify, render_template
import requests
from schemas import DrugRequestSchema
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Access environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Simulated database for drug information
drug_database = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/drugs', methods=['POST'])
def get_drug_info():
    schema = DrugRequestSchema()
    try:
        if request.form.get('drug_names'):
            drug_names = request.form.get('drug_names').split(',')
        else:
            drug_names = request.json.get('drug_names', [])
        
        data = {'drug_names': drug_names}
        schema.load(data)
        
    except Exception as err:
        logger.error(f"Validation error: {err}")
        return jsonify({"error": str(err)}), 400

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
                    logger.warning(f"Drug not found: {drug_name}")
            else:
                info = {"error": "Failed to fetch drug information"}
                logger.error(f"Failed to fetch drug information for {drug_name}")
        all_drug_info.append({drug_name: info})
    
    return render_template('drug_info.html', drug_info=all_drug_info, side_effects=list(all_side_effects))

@app.route('/drugs', methods=['PUT'])
def update_drug_info():
    schema = DrugRequestSchema()
    try:
        data = request.json
        schema.load(data)
        
        drug_name = data['drug_name']
        updated_info = data['updated_info']
        
        if drug_name not in drug_database:
            logger.warning(f"Drug not found in database: {drug_name}")
            return jsonify({"error": "Drug not found in database"}), 404
        
        drug_database[drug_name].update(updated_info)
        logger.info(f"Drug information for {drug_name} updated successfully")
        
        return jsonify({"message": f"Drug information for {drug_name} updated successfully", "updated_info": drug_database[drug_name]})
    
    except Exception as err:
        logger.error(f"Error updating drug information: {err}")
        return jsonify({"error": str(err)}), 400

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    logger.error("Page not found")
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error("Internal server error")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
