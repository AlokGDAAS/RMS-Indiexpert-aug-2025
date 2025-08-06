import json
import os
import uuid
import datetime
import sys
import msvcrt
import bcrypt
from .user_model import User



class AuthSystem:
    def __init__(self,users_auth_data_file,login_logs_file):    

        self.users_auth_data_file = users_auth_data_file            
        self.log_in_logs_file = login_logs_file

        self.users_auth_data = self.load_datadict(self.users_auth_data_file)
        
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

    def save_data(self,data_file,data):
        with open(data_file,"w")as file:
            json.dump(data, file, indent=4)
            


    def get_password(self,prompt="Password: "):
            print(prompt, end='', flush=True)
            password = ''
            while True:
                char = msvcrt.getch()
                if char in {b'\r', b'\n'}:  # Enter key pressed
                    print()
                    break
                elif char == b'\x08':  # Backspace pressed
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    password += char.decode('utf-8')
                    sys.stdout.write('*')
                    sys.stdout.flush()
            return password

    def save_users(self):        
            self.save_data(self.users_auth_data_file, self.users_auth_data)

            
    def hash_password(self, plain_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')   
    
    def check_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


    def signup_verification(self,user_name,user_password,confirm_password,admin_name=None,admin_password=None,role="staff"):  

        if not self.users_auth_data =={}:      

            if admin_name not in self.users_auth_data:
                print("wrong admin name")
                return        
            
            if not self.check_password(admin_password, self.users_auth_data[admin_name]["password"]):
                print("Incorrect admin password")
                return      

        if user_name  in self.users_auth_data:
            print("user name already exist ! Try a diffrent one ")
            return    

        if user_password != confirm_password:
            print("password do not match !")
            return
        
        new_user =User(user_name,self.hash_password(user_password),role)

        self.users_auth_data[user_name] = new_user.to_dict()
        self.save_users()
        print(f"{user_name} save as {self.users_auth_data[user_name]["role"]} ")  
        self.log_action(f"{user_name} signed in as {self.users_auth_data[user_name]["role"]}") 

    def sign_up(self):
                if not self.users_auth_data == {}:

                    print("\nOnly admin is authorised to signing up staff so fisrt login as admin\n")
                    admin_name = input("Enter admin name : ")
                    admin_password = self.get_password("Enter admin password : ") 
                    user_name = input("Enter user name : ")
                    user_password = self.get_password("Enter user password : ")   
                else:
                    admin_name = input("Enter admin name : ")
                    admin_password = self.get_password("Enter admin password : ")  
                    user_name = admin_name
                    user_password = admin_password


                confirm_password = self.get_password("confirm password : ")  
                role=input("Enter role  admin/staff : ")
                self.signup_verification(user_name,user_password,confirm_password,admin_name,admin_password,role)        
            


    def signout(self,user_name,user_password):
         
        
        if user_name not in self.users_auth_data:
                print("user does not exist")
                return

        if not self.check_password(user_password, self.users_auth_data[user_name]["password"]):
            print("Wrong user password")
            return
        
        del self.users_auth_data[user_name]
        self.save_users()
        print(f"{user_name} signed out successfully") 
        self.log_action(f"{user_name} signed out ") 
  


    def login_verification(self,user,password):
       
      
        if user not in self.users_auth_data:
            print("user name does not exist")
            return        
        
        if not self.check_password(password, self.users_auth_data[user]["password"]):
            print("Incorrect password")
            return    
    
               

    
        
        print(f"Role:- {self.users_auth_data[user]["role"]}")
        print(f"Hi {user} you are most weicome !")
        self.log_action(f"{user} logged in as {self.users_auth_data[user]["role"]}")
        
        return True
    
    def login(self):

        user = input("Enter user name : ")
        password = self.get_password("Enter user password : ")
        if self.login_verification(user,password):
            return True 


    def change_name_password(self,user_name,user_password):

        old_name = user_name
      
        if user_name not in self.users_auth_data:
            print("User name does not exist")
            return

       
        if not self.check_password(user_password, self.users_auth_data[user_name]["password"]):
            print("Incorrect password")
            return

 
        new_name = None
        new_password = None

        choice1 = input("Change user name --> yes/no: ").strip().lower()
        if choice1 == "yes":
            new_name = input("New user name: ").strip()
            if not new_name:
                print("New user name cannot be empty")
                return

        choice2 = input("Change password --> yes/no: ").strip().lower()
        if choice2 == "yes":
            new_password = self.get_password("New password: ")
            confirm = self.get_password("Confirm new password: ")
            if new_password != confirm:
                print("Passwords do not match")
                return

        if new_name:
       
            self.users_auth_data[new_name] = self.users_auth_data.pop(user_name)
            user_name = new_name  # Update `user` to new name
            print("Username changed successfully")
            self.log_action(f"{old_name} changed his/her user name as {new_name}")

        if new_password:
            self.users_auth_data[user_name]["password"] = self.hash_password(new_password)
            print("Password changed successfully")
            self.log_action(f"{old_name} which is now {new_name} changed his/her password")

        if not new_name and not new_password:
            print("No changes made.")
            return

        self.save_users()
        print(f"Welcome {user_name}!")

    def profile(self):    
            print("1. Change profile")
            print("2. Delete profile")
            while True:
                choice=input("Choose an option : ")
                if choice == "1":
                    user_name = input("Enter user name : ")
                    user_password = self.get_password("Enter user password : ")  
                    self.change_name_password(user_name,user_password)                    
                    break
                elif choice == "2":
                    user_name = input("Enter user name : ")
                    user_password = self.get_password("Enter user password : ")                
                    self.signout(user_name,user_password)
                    break
                else:
                    print("Please try again later")            

        
   
    def log_action(self, action):
       
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{time}] {action}\n"
        with open(self.log_in_logs_file, 'a') as f:
            f.write(entry)


  









