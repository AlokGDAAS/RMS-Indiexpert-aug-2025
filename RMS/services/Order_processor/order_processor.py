import json
import os
import datetime
import uuid


class Order_Handler:
    def __init__(self,
                 users_auth_data_file,               
                 menu_data_file,
                 booked_orders_data_file,                
                 table_data_file
                 ):
       
        self.users_auth_data_file = users_auth_data_file        
        self.menu_data_file = menu_data_file       
        self.booked_orders_data_file = booked_orders_data_file          
        self.table_data_file = table_data_file      

       
        self.users_auth_data= self.load_datadict(self.users_auth_data_file)       
        self.menu_data = self.load_datalist(self.menu_data_file)
        self.booked_orders_data = self.load_datalist(self.booked_orders_data_file)        
        self.table_data = self.load_datalist(self.table_data_file)

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
        
    def load_datadict(self, data_file):
        if not os.path.exists(data_file):
            return {}
        try:
            with open(data_file, "r") as file:
                data = json.load(file)
                return data if data else {}
        except json.JSONDecodeError:
            print("Error reading JSON. Starting with empty data.")
            return {}   

    def save_booked_order(self):
        with open(self.booked_orders_data_file, "w") as file:
            json.dump(self.booked_orders_data, file, indent=4)
        print("order booked successfully.")



    def item_list(self):
        item_list =[]
        for i in self.menu_data:
            item_list.append(i["name"])
        return item_list
    
    def item_size(self):
        size_dict = {}
        for item in self.menu_data:
            sizes = [size for size, price in item["price"].items() if price != "N.A."]
            size_dict[item["name"]] = sizes
        return size_dict      
        
    def show_keys(self):
        if self.menu_data:
            return list(self.menu_data[0].keys())
        return []


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
            print(f"{'Name':<12} {'Quarter':<8} {'Half':<8} {'Full':<8}")
            for item in categories[category]:
                name = item['name']
                quarter = item['price']['quarter'] + "/-"
                half = item['price']['half'] + "/-"
                full = item['price']['full'] + "/-"
                print(f"{name:<12} {quarter:<8} {half:<8} {full:<8}")   

    def show_tables(self):
        print("\n=== TABLE STATUS ===")
        print(f"{'Table No.':<10} {'Size':<12} {'Current-status':<15} {'Adce book':<10} {'Booking Details'}")
        print("-" * 90)

        for table in self.table_data:
            table_no = table.get("table-no")
            table_size = table.get("table-size")
            bookings = table.get("booking-status", [])

            current_status = "Available"

            # Check live orders
            for order in self.booked_orders_data:
                if order["table_no"] == table_no:
                    current_status = "Occupied"
                    break

            adce_book = "yes" if bookings else "no"

            if bookings:
                for booking in bookings:
                    print(f"{table_no:<10} {table_size:<12} {current_status:<15} {adce_book:<10} "
                        f"ID: {booking.get('booking_id', '-')}, "
                        f"Date: {booking.get('date', '-')}, "
                        f"Time: {booking.get('start-time', '-')}-{booking.get('end-time', '-')}")
                    table_no, table_size, current_status, adce_book = "", "", "", ""
            else:
                print(f"{table_no:<10} {table_size:<12} {current_status:<15} {adce_book:<10}")

        print("-" * 90)



    
    def show_current_orders(self):
        print("\n=== CURRENT ORDERS ===\n")
        for order in self.booked_orders_data:
            print(f"Order ID   : {order['id']}")
            print(f"Table No   : {order['table_no']}")
            print(f"Date       : {order['createddate']} {order['createdtime']}")
            print(f"Items      :")
            for item in order['item']:
                print(f"   - {item['name']} ({item['size']}) x {item['quantity']}")
            print("-" * 40)

    def show_table_order(self):
        list=[]
        for i in self.booked_orders_data:                
                  id=i["id"]  
                  table_no=i["table_no"]
                  note=f"order id {id} is on table-no {table_no}"  
                  list.append(note)
        for j in list:
            print(j)   

    def idwise_order(self,order_id):
        for order in self.booked_orders_data:
            if order["id"]==order_id:     
                print(f"\nOrder ID   : {order['id']}")
                print(f"Table No   : {order['table_no']}")
                print(f"Date       : {order['createddate']} {order['createdtime']}")
                print(f"Items      :")
                for item in order['item']:
                    print(f"   - {item['name']} ({item['size']}) x {item['quantity']}")
                print("-" * 40,"\n")



    def book_orders(self):  
        self.show_tables()     
        item_list = self.item_list()
        item_size = self.item_size()        
        
        ordtyp = input("Press 1. for New order\nPress 2. for Existing order : ")
        if ordtyp =="1":
            order={}        
            order["id"]=uuid.uuid4().hex[:4]
            order["table_no"] = input("Table no: ")
            order["createddate"]= datetime.datetime.now().strftime("%d-%m-%Y")
            order["createdtime"]= datetime.datetime.now().strftime("%H:%M:%S")
            order["item"]=[]
            self.show_menu()
            i = 0
            while(True):
                if i >0:
                    next=input("next item --> yes/no : ")
                    if next == "yes":
                        pass
                    elif next =="no":
                        break
                    else:
                        print("Please enter a right input")
                while True:           
                    name=input(f"item {i+1} name : ")
                    if name in item_list:
                        break
                    else:
                        print(f"{name} not available try another item " )
                        print("Available items : \n" )
                        for item in item_list:print(item)
                while True:
                    print(f"Available size of {name}")
                    for j in item_size[name]:
                        print(j)
                    print()    
                    size=input(f"size of {name} : ")
                    if size not in item_size[name]:
                            print("This size is not available")
                        
                    else:
                        break
                
                quantity=input(f"quantity of {size} {name} : ") 
                dict={"name":name,"size":size,"quantity":quantity}            
                order["item"].append(dict)  
                i += 1     
            self.booked_orders_data.append(order)              
            print("\n=== CURRENT ORDERS ===\n")               
            print(f"Order ID   : {order['id']}")
            print(f"Table No   : {order['table_no']}")
            print(f"Date       : {order['createddate']} {order['createdtime']}")
            print(f"Items      :")
            for item in order['item']:
                print(f"   - {item['name']} ({item['size']}) x {item['quantity']}")
                print("-" * 40)
                                           
            self.save_booked_order() 
        elif ordtyp =="2":
            self.show_table_order()
            order_id=input("Order-id : ")
            for order in self.booked_orders_data:
                if order["id"] == order_id:                    
                    self.show_menu()
                    i = 0
                    while(True):
                        if i >0:
                            next=input("next item --> yes/no : ")
                            if next == "yes":
                                pass
                            elif next =="no":
                                break
                            else:
                                print("Please enter a right input")
                        while True:           
                            name=input(f"item {i+1} name : ")
                            if name in item_list:
                                break
                            else:
                                print(f"{name} not available try another item " )
                                print("Available items : \n" )
                                for item in item_list:print(item)
                        while True:
                            print(f"Available size of {name}")
                            for j in item_size[name]:
                                print(j)
                            print()    
                            size=input(f"size of {name} : ")
                            if size not in item_size[name]:
                                    print("This size is not available")
                                
                            else:
                                break
                        
                        quantity=input(f"quantity of {size} {name} : ") 
                        dict={"name":name,"size":size,"quantity":quantity}            
                        order["item"].append(dict)  
                        i += 1                     
                    print("\n=== CURRENT ORDERS ===\n")               
                    print(f"Order ID   : {order['id']}")
                    print(f"Table No   : {order['table_no']}")
                    print(f"Date       : {order['createddate']} {order['createdtime']}")
                    print(f"Items      :")
                    for item in order['item']:
                        print(f"   - {item['name']} ({item['size']}) x {item['quantity']}")
                        print("-" * 40)
            self.save_booked_order() 
        else:
            print("wrong input")
            return
            

   


    def delete_orders(self, del_id):
        for i, order in enumerate(self.booked_orders_data):
            if order.get("id") == del_id:
                del self.booked_orders_data[i]
                self.save_booked_order()
                return True
        return False

    def main(self):


        while True:
            print("\n==== Menu Handler ====")
            print("1. Book order")
            print("2. Show table")  
            print("3. Cancel order")
            print("4. Show all booked orders")
            print("5. Exit")
    
            choice = input("Choose an option: ")

            if choice == "1":
                self.book_orders()


            elif choice == "2":
                self.show_tables()

            elif choice == "3":
                self.show_current_orders()
                order_id = input("Enter order id which order you want to cancel : ")                
                success = self.delete_orders(order_id)
                if success:
                    print("Order canceled successfully.")
                else:
                    print("Order ID not found.")

            elif choice == "4":
                print("All booked orders :")
                self.show_current_orders()

            elif choice == "5":
                print("Goodbye!")
                break


            else:
                print("Invalid choice. Try again.")




