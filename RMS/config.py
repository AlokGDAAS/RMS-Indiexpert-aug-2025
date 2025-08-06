import os


BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DATA_DIR =os.path.join(BASE_DIR ,"database")

USERS_DIR = os.path.join(DATA_DIR,"users_auth.json")
MENU_DIR = os.path.join(DATA_DIR,"menu_items.json")
ORDERS_DIR = os.path.join(DATA_DIR,"booked_orders_data.json")
TABLES_DIR = os.path.join(DATA_DIR,"table_data.json")
BOOKED_TABLES_DIR = os.path.join(DATA_DIR,"table_booking_data.json")
BILL_DIR = os.path.join(DATA_DIR,"bill_data.json")
CATE_DIR = os.path.join(DATA_DIR,"categories.json")




LOGIN_LOGS_DIR = os.path.join(DATA_DIR,"login_logs.txt")
ERROR_LOGS_DIR = os.path.join(DATA_DIR,"error_logs.txt")
TABLE_BOOKING_LOGS_DIR = os.path.join(DATA_DIR,"table_booking_logs.txt")
