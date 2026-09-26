import requests
# Install requests from the VScode terminal with: "pip install requests"

# Import UI code
# from ui.search_view_edit import SearchViewEdit
from ui.login_view import LoginView
from ui.add_item_view import AddItemView
from ui.remove_item_view import RemoveItemView
from ui.manage_fields_view import ManageFieldsView
# Import Database Code
from database.DatabaseSystem import *

class AI:
    def __init__(self, inventory_system):
        self.inventory_system = inventory_system
        # note: api key was hardcoded into the source code for simplicity, since this 
        # is an academic project and security isn't a concern.
        self.api_key_gemini = "<>"
        self.api_url = f"<>"
        # ----------------------------------------
        
    def make_Query(self, user_query):
        print("CALL TO AI")
        # Construct the API request payload
        payload = {
            "contents": [{
                "parts": [
                    {"text": "You are a database assistant. Answer the user's questions based on the provided database snapshot."
                    "dont answer any question about the fields"},
                    {"text": "If specifically prompted to use a function, you MUST return ONLY the function requested:" + 
                     " function: 'show_ids', use: will show the user the items which ids are included in the list of integers, here is an example of what you would say to show the user the items of id=1 and id=15: 'show_ids: [1,15]'"},
                    {"text": str(user_query)},
                    {"text": f"Database snapshot:\n{self.get_database_json()}"}
                ]
            }]
        }

        headers = {"Content-Type": "application/json"}

        # Make the API request
        response = requests.post(self.api_url, headers=headers, json=payload)

        # Parse and return response
        if response.status_code == 200:
            response_data = response.json()
            response = response_data["candidates"][0]["content"]["parts"][0]["text"]
            try:
                print(response)
                if "show_ids" in response:
                    ids_str = response.split("show_ids:")[1].strip()  # Extract the part after "show_ids:"
                    ids_list = eval(ids_str)  # Converts a string "[1, 4, 6]" into a Python list
                    return self.inventory_system.get_products_by_id(ids_list)
                    
                return response
            except (KeyError, IndexError):
                return "Error: Unexpected response format."
        else:
            return f"Error: API request failed with status code {response.status_code}"
            
    def get_database_json(self):
        try:
            database_items = self.inventory_system.get_all_items()
            database_json = database_items.to_json(orient="records", indent=4)
            return database_json
        except Exception as e:
            print("ERROR WITH DATABASE")
            return f"Error retrieving database: {str(e)}"
            
