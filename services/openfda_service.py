import requests

def search_drug(drug_name):
    url = "https://api.fda.gov/drug/ndc.json?"
    query = f'search=generic_name:"{drug_name}"'
    # Full API URL
    api_url = url + query

    try:
        # GET request to OpenFDA API
        response = requests.get(api_url)

        # Checks if it's a 200 status code, if it's any other status code like 400 there would be an error
        if response.status_code == 200:
            data = response.json()

            # Checking our data to see if it actually found results
            if 'results' in data and data['results']:
                results_list = []
                for result in data['results']:
                    # The specific fields that we want to extract
                    product_ndc = result.get('product_ndc', 'N/A')      
                    brand_name = result.get('brand_name', 'N/A')
                    dosage_form = result.get('dosage_form', 'N/A')
                    active_ingredients = result.get('active_ingredients',[])

                    ingredients_list = []
                    if active_ingredients:
                        for ingredient in active_ingredients:
                            name = ingredient.get('name', 'N/A')
                            strength = ingredient.get('strength', 'N/A')
                            if isinstance(strength, list):
                                strength = ", ".join(strength)
                            ingredients_list.append({"name": name, "strength": strength})

                    results_list.append({
                        "Product NDC": product_ndc,
                        "Brand Name": brand_name,
                        "Dosage Form": dosage_form,
                        "Active Ingredients": ingredients_list
                    })
                return {"drug_name": drug_name, "results": results_list}
            else:
                return {"drug_name": drug_name, "message": "No results found"}
        else:
            return {"drug_name": drug_name, "message": f"Error: Status code {response.status_code}", "error": response.text}

    except requests.exceptions.RequestException as e:
        return {"drug_name": drug_name, "message": "Request failed", "error": str(e)}
