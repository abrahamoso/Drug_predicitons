from flask import Blueprint, request, jsonify
from controllers.drug_controller import get_drug_info, add_drug, delete_drug, search_drugs

drugs_bp = Blueprint('drugs', __name__)

@drugs_bp.route('/', methods=['GET'])
def get_drugs():
    return get_drug_info()

@drugs_bp.route('/', methods=['POST'])
def create_drug():
    data = request.json
    return add_drug(data)

@drugs_bp.route('/<drug_id>', methods=['DELETE'])
def remove_drug(drug_id):
    return delete_drug(drug_id)

@drugs_bp.route('/search', methods=['POST'])
def search_drugs_endpoint():
    data = request.json
    drug_names = data.get('drug_names', [])
    return search_drugs(drug_names)
