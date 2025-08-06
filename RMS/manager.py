import json
import datetime
import traceback

from services.User_authentication.user_authentication import AuthSystem
from services.Table_booking.table_booking import Table_Handler
from services.Order_processor.order_processor import Order_Handler
from services.Menu_handler.menu_handler import Menu_Handler
from services.Bill_generator.bill_generator import Bill_Handler
from services.Reports.reports import Reports_Handler
import config


class Manager:
    def __init__(self):
        self.users_auth_data_file = config.USERS_DIR
        self.table_data_file = config.TABLES_DIR
        self.table_booking_data_file = config.BOOKED_TABLES_DIR
        self.booked_orders_data_file = config.ORDERS_DIR
        self.menu_data_file = config.MENU_DIR
        self.category_data_file = config.CATE_DIR
        self.bill_data_file = config.BILL_DIR

        self.log_in_logs_file = config.LOGIN_LOGS_DIR
        self.table_booking_logs_file = config.TABLE_BOOKING_LOGS_DIR
        self.error_logs_file = config.ERROR_LOGS_DIR


        self.auth_system = AuthSystem(self.users_auth_data_file, self.log_in_logs_file)
        self.menu_manager = Menu_Handler(self.menu_data_file, self.category_data_file)
        self.order_manager = Order_Handler(self.users_auth_data_file, self.menu_data_file,
                                           self.booked_orders_data_file, self.table_data_file)
        self.table_manager = Table_Handler(self.table_data_file, self.table_booking_data_file,
                                           self.booked_orders_data_file, self.table_booking_logs_file)
        self.bill_manager = Bill_Handler(self.users_auth_data_file, self.menu_data_file,
                                         self.booked_orders_data_file, self.bill_data_file)
        self.reports_manager = Reports_Handler(self.bill_data_file, self.menu_data_file)

    def run(self):
        print("\n==================== Welcome to Kailash Restaurant ===============================\n")
        try:
            while True:
                print("\n===== Main Menu =====")
                print("1. Sign Up")
                print("2. Log in")
                print("3. Exit")

                choice = input("Choose an option number or name: ").strip().lower()

                if choice in ("1", "sign up", "signup"):
                    self.auth_system.sign_up()

                elif choice in ("2", "log in", "login"):
                   
                    user = self.auth_system.login()
                    if not user:
                        print("Login failed — try again.")
                        continue

                    
                    while True:
                        print(f"\nLogged in as: {getattr(user, 'username', user)}")
                        print("1. Menu handling")
                        print("2. Table booking")
                        print("3. Order Processing")
                        print("4. Bills")
                        print("5. Reports")
                        print("6. Profile")
                        print("7. Logout")

                        sub = input("Choose an option: ").strip().lower()

                        if sub in ("1", "menu", "menu handling"):
                            self.menu_manager.main()
                        elif sub in ("2", "table", "table booking"):
                            self.table_manager.main()
                        elif sub in ("3", "order", "order processing"):
                            self.order_manager.main()
                        elif sub in ("4", "bills", "bill"):
                            self.bill_manager.main()
                        elif sub in ("5", "reports"):
                            self.reports_manager.generate_report()
                        elif sub in ("6", "profile"):
                            self.auth_system.profile()
                        elif sub in ("7", "logout", "exit"):
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice in authenticated menu.")

                elif choice in ("3", "exit", "quit"):
                    print("Goodbye — thank you! Visit again.")
                    break

                else:
                    print("Please enter a valid input (1, 2, or 3).")

        except json.JSONDecodeError as e:
            with open(self.error_logs_file, "a") as log:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{now} - JSONDecodeError: {str(e)}\n")
                traceback.print_exc(file=log)
                log.write("\n")
            print("Error reading JSON. Starting with empty data.")

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting gracefully.")

        except Exception as e:
         
            with open(self.error_logs_file, "a") as log:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"{now} - Unexpected error: {str(e)}\n")
                traceback.print_exc(file=log)
                log.write("\n")
            print("An unexpected error occurred. Check logs.")


if __name__ == "__main__":
    manager = Manager()
    manager.run()

    
 


     







