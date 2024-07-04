from flask import jsonify

def get_drug_info():
    return jsonify({"message": "Fetching drug information"})

def add_drug(data):
    return jsonify({"message": "Drug added", "data": data})

def delete_drug(drug_id):
    return jsonify({"message": f"Drug {drug_id} deleted"})

def search_drugs(drug_names):
    results = [{"name": drug_name, "info": "Sample info"} for drug_name in drug_names]
    return jsonify(results)
