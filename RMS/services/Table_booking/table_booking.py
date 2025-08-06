from datetime import datetime ,timedelta
import json
import os
import uuid

class Table_Handler:
    def __init__(self, table_data_file, table_booking_data_file,booked_orders_data_file,table_booking_logs_file):
        self.table_data_file = table_data_file
        self.table_booking_data_file = table_booking_data_file
        self.table_booking_logs_file = table_booking_logs_file
        self.booked_orders_data_file = booked_orders_data_file
        self.table_data = self.load_datalist(self.table_data_file)
        self.table_booking_data = self.load_datalist(self.table_booking_data_file)
        self.booked_orders_data = self.load_datalist(self.booked_orders_data_file)

    def load_datalist(self, data_file):
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

    def save_booked_table(self):
        with open(self.table_booking_data_file, "w") as file:
            json.dump(self.table_booking_data, file, indent=4)
        print("Booking data saved.")

    def save_table_data(self):
        with open(self.table_data_file, "w") as file:
            json.dump(self.table_data, file, indent=4)
        print("Table data saved.")
        

    def show_tables(self):
        print("\n================================== TABLE STATUS ============================================\n")
        print(f"{'Table No.':<10} {'Size':<12} {'Current-status':<15} {'Advce book':<10} {'Booking Details'}")
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


    def show_keys(self, item):
        return list(item.keys()) if item else []

    def book_table(self):
        while True:
            booking = {
                "booking_id": uuid.uuid4().hex[:4],
                "customer_name": input("Customer name: ").strip(),
                "customer_phone": input("Customer phone: ").strip(),
                "created_date": datetime.now().strftime("%d-%m-%Y"),
                "created_time": datetime.now().strftime("%H:%M")
            }
            self.show_tables()

            # Select table
            while True:
                table_no = input("Please provide table number: ").strip()

                matched_table = next((t for t in self.table_data if t["table-no"] == table_no), None)

                if not matched_table:
                    print("Table number not found. Try again.")
                    continue

                print(f"Table size: {matched_table['table-size']}")
                choice = input("1: Proceed, 2: Change Table: ").strip()

                if choice == "1":
                    booking["table_no"] = table_no
                    booking["table_size"] = matched_table["table-size"]
                    break
                elif choice == "2":
                    continue
                else:
                    print("Invalid input.")

            # Booking date
            while True:
                date = input("Booking date (dd-mm-yyyy): ").strip()
                try:
                    booking_date = datetime.strptime(date, "%d-%m-%Y").date()
                    today = datetime.now().date()
                    upto = (datetime.now() + timedelta(days=90)).date()
                    if booking_date < today:
                        print("Date cannot be in the past. Try again.")
                    elif booking_date > upto :
                        print(f"Booking available upto 90 days from today i.e. till {upto}")    
                    else:
                        break
                except ValueError:
                    print("Invalid format. Use dd-mm-yyyy.")

            # Time slot — moved **outside** date loop
            slot = {
                "booking_id": booking["booking_id"],
                "date": date
            }

            # Start time
            while True:
                start_time_str = input("Start time (HH:MM): ").strip()
                try:
                    start_time = datetime.strptime(start_time_str, "%H:%M").time()
                    if not (datetime.strptime("09:00", "%H:%M").time() <= start_time <= datetime.strptime("22:00", "%H:%M").time()):
                        print("Booking time must be between 09:00 and 22:00")
                    else:
                        slot["start-time"] = start_time_str
                        break
                except ValueError:
                    print("Invalid time format.")

            # End time
            while True:
                end_time_str = input("End time (HH:MM): ").strip()
                try:
                    end_time = datetime.strptime(end_time_str, "%H:%M").time()
                    if not (datetime.strptime("09:00", "%H:%M").time() <= end_time <= datetime.strptime("22:00", "%H:%M").time()):
                        print("Booking time must be between 09:00 and 22:00")
                    else:
                        slot["end-time"] = end_time_str
                        break
                except ValueError:
                    print("Invalid time format.")

            # Check start < end
            new_start = datetime.strptime(slot["date"] + " " + slot["start-time"], "%d-%m-%Y %H:%M")
            new_end = datetime.strptime(slot["date"] + " " + slot["end-time"], "%d-%m-%Y %H:%M")

            if new_start >= new_end:
                print("End time must be after start time.")
                continue

            # Check conflicts
            conflict = False
            for existing in matched_table.get("booking-status", []):
                if existing["date"] == slot["date"]:
                    exist_start = datetime.strptime(existing["date"] + " " + existing["start-time"], "%d-%m-%Y %H:%M")
                    exist_end = datetime.strptime(existing["date"] + " " + existing["end-time"], "%d-%m-%Y %H:%M")
                    if new_start < exist_end and new_end > exist_start:
                        print("Conflict! Table is not available for this slot. Try another time slot.")
                        conflict = True
                        break

            if conflict:
                continue

            booking["booking_date_time"] = slot
            matched_table.setdefault("booking-status", []).append(slot)

            self.table_booking_data.append(booking)
            self.save_booked_table()
            self.save_table_data()
            print(f"Booking {booking['booking_id']} created successfully!")
            self.log_action(f"table no {booking['table_no']}, booked with id {booking['booking_id']} for {booking['customer_name']} phone {booking['customer_phone']}  ")

            if input("Book another table? (yes/no): ").strip().lower() != "yes":
                break
            
   
    def cancel_booking(self):
        self.show_tables()
        booking_id = input("Booking ID to cancel: ").strip()
        reason_list=["Bad behavior","Connectivity issue","Bad service","Expensive","Extra Charges","Other"]
        for booking in self.table_booking_data:
            if booking["booking_id"]  == booking_id:
                print("\n Reason for cancellation")
                for j , r in enumerate(reason_list):
                    print(f"{j+1}.{r}")
                choice= input("Please provide a reason for cancellation : ")
                reason=reason_list[int(choice)-1]
        self.log_action(f"booking of table no {booking['table_no']}, with id {booking['booking_id']} cancelled by {booking['customer_name']}, phone {booking['customer_phone']} ,reason :- {reason}")
        self.table_booking_data = [
            b for b in self.table_booking_data if b["booking_id"] != booking_id
        ]

        for table in self.table_data:
            table["booking-status"] = [
                s for s in table["booking-status"] if s["booking_id"] != booking_id
            ]
        

        self.save_booked_table()
        self.save_table_data()
        print(f"Booking {booking_id} cancelled.")

    def log_action(self, action):
       
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{time}] {action}\n"
        with open(self.table_booking_logs_file, 'a') as f:
            f.write(entry)


       

    def main(self):

 

        while True:
            print("\n==== Table booking ====")
            print("1. Book table in Advance")
            print("2. Show table")      
            print("4. Cancel booking")
            print("5. Back to main menu")

            choice = input("Choose an option: ")
            if choice == "1":
                self.book_table()
            elif choice == "2":
                self.show_tables()
            elif choice == "3":
                self.update_book_table()
            elif choice == "4":
                self.cancel_booking()
            elif choice == "5":
                break
            else:
                print("Please enter a right input")


# table = Table_Handler("table_data.json","table_booking_data.json","booked_orders_data.json")           
            
            





    



    
       

                     





            
