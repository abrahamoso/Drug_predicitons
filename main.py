import requests

def search_drug():
    url = "https://api.fda.gov/drug/ndc.json?"
    # Created a list to collect multiple drug names from the user
    drugs = []
    
    # Ask user to enter the drug name
    while True:
        drug_name = input('Enter the name(s) of the drug to search (type "done" to finish): ')
        if drug_name.lower() == 'done':
            break
        drugs.append(drug_name)

    for drug_name in drugs:
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
                    print(f"\nResults for drug '{drug_name}':\n")
                    for result in data['results']:
                        # The specific fields that we want to extract
                        product_ndc = result.get('product_ndc', 'N/A')      
                        brand_name = result.get('brand_name', 'N/A')
                        dosage_form = result.get('dosage_form', 'N/A')
                        active_ingredients = result.get('active_ingredients',[])

                        print(f"Product NDC: {product_ndc}")
                        print(f"Brand Name: {brand_name}")
                        print(f"Dosage Form: {dosage_form}")
                        
                        if active_ingredients:
                            print("Active Ingredients:")
                            for ingredient in active_ingredients:
                                name = ingredient.get('name', 'N/A')
                                strength = ingredient.get('strength', 'N/A')
                                if isinstance(strength, list):
                                    strength = ", ".join(strength)
                                print(f"  - Name: {name}, Strength: {strength}")
                        print("\n" + "-"*40 + "\n")
                else:
                    print(f"No results found for drug: {drug_name}")
            else:
                print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
                print(f"Error message: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to make a request to the API. Details: {str(e)}")

# Call the function to execute the search
search_drug()
