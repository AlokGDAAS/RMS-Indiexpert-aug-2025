import json
import os
import datetime
import uuid


class Menu_Handler:
    def __init__(self, menu_data_file,category_data_file):

        self.menu_data_file = menu_data_file
        self.category_data_file = category_data_file
        self.menu_data = self.load_datalist(self.menu_data_file)
        self.category_data = self.load_datalist(self.category_data_file)

    def load_datalist(self,data_file):
        if not os.path.exists(data_file):
            print(f"{data_file} not found. Starting with empty data.")
            return []
        try:
            with open(data_file, "r") as file:
                data = json.load(file)
                return data if data else []
        except json.JSONDecodeError:
            print("Error reading JSON. Starting with empty data.")
            return []       
  

    def save_data(self):
        with open(self.menu_data_file, "w") as file:
            json.dump(self.menu_data, file, indent=4)
        print("Data saved successfully.")

    def save_categories(self):
        with open(self.category_data_file, "w") as file:
            json.dump(self.category_data, file, indent=4)
        print("Data saved successfully.")



    def show_keys(self, data):
        if not data:
            return []
        elif isinstance(data, list):
            if len(data) == 0:
                return []
            return list(data[0].keys())
        elif isinstance(data, dict):
            return list(data.keys())
        else:
            return []
        

    def show_item_id(self):
            print("-"*50)
            print("     All Items id    ")
            print("-"*50)
            print("name:              id              category")
            print("-"*50)
            for item in self.menu_data:
                print(f"{item["name"]:<20} : {item["item_id"]:<8} {item["category"]}")  
            print("-"*50)   
    


    

    def edit_categories(self):
        while True:
            print("1. Add new category")
            print("2. Change existing category")
            print("3. Exit")
            choice = input("Choose an option: ").strip()

            categories = self.category_data

            if choice == "1":
                add = input("Please provide a new category: ")
                categories.append(add)
                self.save_categories(categories)
                print("Category added.")
            elif choice == "2":
                existing = input("Which category name do you want to change? ")
                new = input("New name: ")
                for idx, val in enumerate(categories):
                    if val == existing:
                        categories[idx] = new
                        print(f"Category '{existing}' changed to '{new}'.")
                        break
                else:
                    print("Category not found.")
                self.save_categories(categories)
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")

    def update_menu(self):
        self.show_item_id()
        item_id = input("Please provide item id: ").strip()

        found = False
        for i in self.menu_data:
            if i["item_id"] == item_id:
                found = True
                print("What do you want to update?")
                print("1. Item ID")
                print("2. Name")
                print("3. Price")
                print("4. Category")

                choice = input("Enter your choice: ").lower()

                if choice in ["1", "item id"]:
                    new_id = input("Provide new item id: ").strip()
                    if new_id:
                        i["item_id"] = new_id

                elif choice in ["2", "name"]:
                    new_name = input("Provide new name: ").strip()
                    if new_name:
                        i["name"] = new_name

                elif choice in ["3", "price"]:
                    for size in ["full", "half", "quarter"]:
                        new_price = input(f"Enter new price for {size} (leave blank to keep current): ").strip()
                        if new_price:
                            i["price"][size] = new_price

                elif choice in ["4", "category"]:
                    cat_list = self.category_data
                    for idx, cat in enumerate(cat_list, start=1):
                        print(f"{idx}. {cat}")
                    try:
                        new_cat_index = int(input("Choose a category number: "))
                        if 1 <= new_cat_index <= len(cat_list):
                            i["category"] = cat_list[new_cat_index - 1]
                    except ValueError:
                        print("Invalid category choice.")

                break  # stop loop once found

        if not found:
            print("Item ID not found.")
        else:
            self.save_data()
            print("Updated successfully.")




                  
    


    def add(self, record):
        if not isinstance(record, dict):
            raise ValueError("Record must be a dictionary.")
        if "name" not in record or "price" not in record or "category" not in record:
            raise ValueError("Record must include at least 'name' 'price' and 'category'.")
        record["createdDate"]= datetime.datetime.now().strftime("%d-%m-%Y")
        record["createdTime"]= datetime.datetime.now().strftime("%H:%M:%S")
        self.menu_data.append(record)
        self.save_data()

        return record

    
    def show_menu(self):
        categories = {}     
        for item in self.menu_data:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

    
        print("=" * 15 + " Menu " + "=" * 15)

        for category in categories:
            print(f"\n              {category.upper()}\n")
            print(f"{'Name':<15} {'Quarter':<8} {'Half':<8} {'Full':<8}")
            for item in categories[category]:
                name = item['name'].title()
                quarter = item['price']['quarter'] + "/-"
                half = item['price']['half'] + "/-"
                full = item['price']['full'] + "/-"
                print(f"{name:<15} {quarter:<8} {half:<8} {full:<8}")    

    def delete(self,item_id):
        for i, item in enumerate(self.menu_data):
            if item.get("item_id") == item_id:
                del self.menu_data[i]
                self.save_data()
                return True
        return False

    def main(self):
     

        while True:
            print("\n==== Menu Handler ====")
            print("1. Add Items")     
            print("2. Delete items")
            print("3. Show items id")
            print("4. Show menu")            
            print("5. Update/Edit menu")
            print("6. Back to previous menu")
        
            choice = input("Choose an option: ")

            if choice == "1":
                num = (input("How many items do you want to add : "))
                num=int(num)
                for i in range(int(num)):

                    item_id=uuid.uuid4().hex[:4]
                    while True:
                        name = input(f"Enter item {i+1} name: ").strip().lower()

                        if name in self.menu_data:
                            print("Item already exists.")
                            continue
                        if name:
                            break
                        print("Item name cannot be empty. Please try again.") 


                    full = input(f"Enter full {name} price: ") or "N.A."                  
                    half = input(f"Enter half {name} price: ") or "N.A."  
                    quarter = input(f"Enter quarter {name} price: ") or "N.A."  
                    price = {"full":full,"half":half,"quarter":quarter}

                    print("\n select the category\n")
                    for i,category in enumerate(self.category_data):
                        print(f"{i+1} . {category}")
                    choice = input(f"Please enter a number and select category : ")
                    category=self.category_data[int(choice) - 1]


                    record = {"item_id":item_id,"name": name, "price": price,"category":category}
                    self.add(record)
                    print("\n      Added Item        ")
                    print("---------------------------")
                    print(f"item_id = {item_id}")
                    print(f"name = {name}")              
                    print(f"      Price     ")
                    print(f"full    half    quarter")
                    print(f"{full}      {half}    {quarter}")



            elif choice == "2":

                self.show_item_id()
                item_id = input("Enter item_id : ")  
                success = self.delete(item_id)
                if success:
                    print("Deleted successfully.")
                else:
                    print("Staff ID not found.")

            elif choice == "3":
                self.show_item_id()

            elif choice == "4":
                self.show_menu()           

            elif choice == "5":
                self.update_menu()    
         

            elif choice == "6":
                break
                           
                     

            else:
                print("Invalid choice. Try again.")

