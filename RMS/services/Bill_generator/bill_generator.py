import json
import os
import datetime
import uuid


class Bill_Handler:
    def __init__(self,users_auth_data_file,menu_data_file,booked_orders_data_file,bill_data_file):
       
        self.users_auth_data_file = users_auth_data_file       
        self.menu_data_file = menu_data_file       
        self.booked_orders_data_file = booked_orders_data_file        
        self.bill_data_file = bill_data_file      

       
        self.users_auth_data= self.load_datadict(self.users_auth_data_file)      
        self.menu_data = self.load_datalist(self.menu_data_file)
        self.booked_orders_data = self.load_datalist(self.booked_orders_data_file)
        self.bill_data = self.load_datalist(self.bill_data_file)

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

    def save_bills(self):
        with open(self.bill_data_file, "w") as file:
            json.dump(self.bill_data, file, indent=4)
        print("bill saved successfully.")  


    def show_bill_status(self):
        print("--------------------------------------ongoing---------------------------------------")
        for i in self.booked_orders_data:
            id = i["id"]
            table_no = i["table_no"]
            note = f"Order ID {id} is ongoing on table-no {table_no}"
            print(note)

        print("--------------------------------------pending---------------------------------------")
     

        for k in self.bill_data:
            if k["status"] =="pending":
                    print(
                        f"Order ID {k['id']} - bill generated for {k['customer name']} "
                        f"({k['customer phone']}), payment status: {k['status']}"
                    )
                    
        print("--------------------------------------completed---------------------------------------")

        for k in self.bill_data:
            if k["status"] == "completed":
                # Parse payment date and time
                p_time_date = datetime.datetime.strptime(
                    k["payment date"] + " " + k["payment time"],
                    "%d-%m-%Y %H:%M"
                )
                current_time = datetime.datetime.now()
                diff = current_time - p_time_date
                minutes = diff.total_seconds() / 60

                if minutes < 15:
                    print(
                        f"Order ID {k['id']} - bill generated for {k['customer name']} "
                        f"({k['customer phone']}), payment status: {k['status']}"
                    )

    def show_completed_bill(self):
        print("There are showing completed bills before 15 minutes ")

        for k in self.bill_data:
            if k["status"] == "completed":
                # Parse payment date and time
                p_time_date = datetime.datetime.strptime(
                    k["payment date"] + " " + k["payment time"],
                    "%d-%m-%Y %H:%M"
                )
                current_time = datetime.datetime.now()
                diff = current_time - p_time_date
                minutes = diff.total_seconds() / 60

                if minutes > 15:
                    print(
                        f"Order ID {k['id']} - bill generated for {k['customer name']} "
                        f"({k['customer phone']}), payment status: {k['status']}"
                    )
        
    def show_bill(self):   
        self.show_bill_status()     
        order_id = input("Provide order id for detailed bill : ")

        isongoing= next((s for s in self.booked_orders_data if s["id"]==order_id),None)
        isgenerated=next((t for t in self.bill_data if t["id"]==order_id),None)

        if not isongoing and not isgenerated:
            print("order does not exist")
            return
        elif isongoing:
            print("Bill not generated") 
            choice=input("Are you want to generate bill yes/no :  ")
            if choice =="yes":
               self.generate_bill(order_id) 
               print(f"Bill successfully generated for order id {order_id}")
               return
            else:
                return   

        

        for i in self.bill_data:
            if i["id"] == order_id:
                order = i

        print("\n" + "=" * 15 + " BILL " + "=" * 23)
        print(f"Bill ID   : {order['id']}")
        print(f"Name      : {order['customer name']}")
        print(f"Phone     : {order['customer phone']}")
        print(f"Table No. : {order['table_no']}")
        print(f"Date      : {order['createddate']}")
        print(f"Time      : {order['createdtime']}")
        print(f"Status    : {order['status']}")
        print("=" * 45)

        grand_total = 0
        total_gst = 0  #  accumulate GST
        print(f"{'Item':<12} {'Size':<8} {'Qty':<5} {'Rate':<8} {'Total':<8}")
        print("-" * 45)

        for ordered_item in order["item"]:
            name = ordered_item["name"]
            size = ordered_item["size"].lower()
            qty = int(ordered_item["quantity"])

            item = next((x for x in self.menu_data if x["name"].lower() == name.lower()), None)
            if not item:
                print(f"{name:<12} Not Found")
                continue

            price_str = item["price"].get(size, "N.A.")
            if price_str == "N.A.":
                print(f"{name:<12} Size '{size}' N.A.")
                continue

            rate = float(price_str)
            item_total = rate * qty
            item_gst = (item_total * 18) / 100
            line_total = item_total + item_gst

            total_gst += item_gst  #  add this item's GST
            grand_total += line_total

            print(f"{name:<12} {size:<8} {qty:<5} {rate:<8} {item_total:<8.2f}")

        print("-" * 45)
        print(f"{'Total ':<33} {grand_total - total_gst:.2f}")
        print(f"{'GST':<34} {total_gst:.2f}")
        print(f"{'Grand Total':<33} {grand_total:.2f}")
        print("=" * 45)  

        
        
    def generate_bill(self,id=""):
        self.show_bill_status()
        if id =="":
            order_id = input("Provide order id for generating bill : ").strip()
        else:
            order_id=id 
        print(f"Please provide name and phone for generating bill for order id {order_id}")   
        customer_name = input("Provide customer name: ").strip() or "N.A."
        customer_phone = input("Provide customer phone: ").strip() or "N.A."



        # Check if bill already exists
        existing_bill = next((b for b in self.bill_data if b["id"] == order_id), None)
        if existing_bill:
            print("Bill already generated for this order.")
            return

        # Find the booked order
        order = next((o for o in self.booked_orders_data if o["id"] == order_id), None)
        if not order:
            print("Order not found!")
            return        

        # Calculate totals
        grand_total = 0
        total_gst = 0

        order["customer name"] = customer_name
        order["customer phone"] = customer_phone

        for ordered_item in order["item"]:
            name = ordered_item["name"]
            size = ordered_item["size"].lower()
            qty = int(ordered_item["quantity"])

            item = next((x for x in self.menu_data if x["name"].lower() == name.lower()), None)
            if not item:
                print(f"{name:<12} Not Found in menu.")
                continue

            price_str = item["price"].get(size, "N.A.")
            if price_str == "N.A.":
                print(f"{name:<12} Size '{size}' N.A.")
                continue

            rate = float(price_str)
            item_total = rate * qty
            item_gst = (item_total * 18) / 100
            line_total = item_total + item_gst

            ordered_item["rate"] = rate
            ordered_item["total"] = item_total
            ordered_item["gst"] = item_gst
            ordered_item["total+gst"] = line_total

            grand_total += line_total
            total_gst += item_gst

        order["grand-total"] = f"{grand_total:.2f}"
        order["status"] = "pending"


        # Add to bill data & save
        self.bill_data.append(order)
        self.save_bills()
        found = False
        for item in self.booked_orders_data:
            if item.get("id") == order_id:
                self.booked_orders_data.remove(item)
                found = True
                break

        if found:
            self.save_booked_order()
            print(f"Order {order_id} deleted successfully.")
        else:
            print(f"No order found with ID {order_id}.")       

        print(f"{'Subtotal':<20}: {grand_total - total_gst:.2f}")
        print(f"{'GST (18%)':<20}: {total_gst:.2f}")
        print(f"{'Grand Total':<20}: {grand_total:.2f}")
        print("Bill generated successfully.")



    def pay_bills(self):
            self.show_bill_status()
            print("\nOnly generated bills can be paid.")

            # Find the bill
            order_id = input("Please enter order id for which bill has been generated: ").strip()
            bill = None

            for i in self.bill_data:
                if i["id"] == order_id:
                    bill = i
                    break

            if not bill:
                print("Bill not found.")
                return

            if bill["status"] == "completed":
                print("Payment already completed.")
                return

            print(f"Name: {bill['customer name']} Phone: {bill['customer phone']}")
            print(f"Please complete payment of {bill['grand-total']}")

            # Payment options
            print("\nPayment options")
            print("1. Credit/Debit Card")
            print("2. UPI")
            print("3. Net Banking")
            print("4. Scan QR Code")
            print("5. Cash\n")

            payment_modes = {
                "1": "Credit/Debit Card",
                "2": "UPI",
                "3": "Net Banking",
                "4": "Scan QR Code",
                "5": "Cash",
            }

            while True:
                payment_option = input("Choose a payment option: ").strip()
                mode = payment_modes.get(payment_option)
                if not mode:
                    print("Invalid payment option. Try again.")
                    continue
                break

            # Update and save
            bill["status"] = "completed"
            bill["payment mode"] = mode
            bill["payment date"] = datetime.datetime.now().strftime("%d-%m-%Y")
            bill["payment time"] = datetime.datetime.now().strftime("%H:%M")
            self.save_bills()
            print("Payment done.")

    def main(self):        

        while True:
            print("\n==== Menu Handler ====")
            print("1. Generate bill") 
            print("2. Show bill") 
            print("3. Pay Bill") 
            print("4. Show Completed Bills") 
            print("5. Exit")
            print("6. Check")
            choice = input("Choose an option: ")

            if choice == "1":
                self.generate_bill()
            elif choice == "2":
                self.show_bill()
            elif choice == "3":
                self.pay_bills()
            elif choice == "4":
                self.show_completed_bill()
            elif choice == "5":
                print("Good Bye")
                break
            elif choice == "6":
                self.show_bill_status()
                
            else:
                print("Wrong input") 


