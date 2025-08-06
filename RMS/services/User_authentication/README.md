
AuthSystem

This is user authentication part of my paroject Reataurent management system

It provides basic functionality for secure 

sign up, 
log in, 
sign out, 
update username, and change password, with hashed passwords and activity logging.

---------------------------------------------------------------------------------

Features


User Sign Up

  - Supports registering new users.
  - First user must be an admin.
  - Only Admins can add new staff users by sign in method.
  - Admins can add new admin users also by sign in method.

Secure Passwords
  - Passwords are hashed using `bcrypt` before saving .
  - Plaintext passwords are never stored.

User Log In & Log Out
  - Authenticates using username and password.
  - Verifies hashed passwords.

Update User Info
  - Admin and staff can Change their username password.
  - Change password with confirmation.
  - Logs all changes.

Activity Logging
  - All logins, signups, signouts, and changes are logged with timestamps.
  - Logs are saved to a file for auditing.


Data Persistence

  - User data is stored in JSON files.
  - Easy to read and modify for debugging.

------------------------------------------------------------------------------------

Requirements

- Python 3.x
- `bcrypt` module (install with `pip install bcrypt`)

Note: `msvcrt` is used for password masking and works only on Windows.

------------------------------------------------------------------------------------

Files

- `authsystem.py` — Main class implementation.
- `user_model.py` — `User` model.
- `users_auth.json` — Stores registered users.
- `login_logs.txt` — Stores activity logs.

-------------------------------------------------------------------------------------

How to Run

1. Make sure you have `bcrypt` installed:
   ```bash
   pip install bcrypt
   ```

2. Run the script:
   ```bash
   python authsystem.py
   ```

3. Follow the on-screen menu:
   - `1. Sign Up`
   - `2. Sign Out`
   - `3. Log In`
   - `4. Update User`
   - `5. Exit`

-----------------------------------------------------------------------------------------
Security Notes

- Uses `bcrypt` for strong password hashing.
- Admin controls who can register new staff users.
- Logs all actions for traceability.

--------------------------------------------------------------------------------------------



## 📢 **Improvements**

Future versions may include:
- Cross-platform password input (`getpass`).
- Role-based access control.
- Due to lack of time i can not add some more detailed validations but i will definitly add in next version
- Any imrovement suggestions are most weicome

----------------------------------------------------------------------------------------------------------------


Author

Built with by Alok Kumar

-------------------------------------------------------------------------------------------