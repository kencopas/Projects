"""

Able to check for existing users and create new users using an AES encryption key to store the password. Next funcitonality is a means of generating and storing the AES key securely.
AES key should not be lost, and should not be re-generated if one already exists. Storage might look like a hidden txt or json file.

"""

from utils.sql_utils import safe_connect
import secrets, string

# Single Sign-On class
class SSO:

    """

    Single Sign-On that manages user information via an sql database

    """

    def __init__(self, service_name: str):

        self.service_name = service_name
        self.profile_info = {}
        print(f"Initializing {service_name} Single Sign-On...")

        # Establish database connection with safe_connect
        self.database = safe_connect(user='root', password='password', host='127.0.0.1', database='data')
        
        # Check for credentials table and AES key
        self.status()

    # Check if credentials table or encryption key exist. Create them if they do not exist
    def status(self):
        print("Checking credentials status...")
        
        # Check if credentials table does not exist
        if not self.database.run("DESC credentials"):
            
            print("credentials table does not exist.")
            print("Creating credentials table...")

            # Exit if table creation fails
            if not self.create_credentials():
                exit()

        else:
            print("Credentials table exists.")

        print("Checking key status...")

        if self.read_key()['status'] != 200:
            print("Creating key...")
            
            # Attempt to create encryption key
            if self.create_key() == 200:
                self.read_key()
            else:
                exit()

        return 200

    # Attempt to read encryption key into self.key, return result
    def read_key(self):
        try:
            # Read key file into self.key
            self.key = open('SSO/backend/utils/.key.txt', 'r').read()
            if self.key:
                return {"message": "Successfully read key!", "status": 200}
            else:
                self.create_key()
        except Exception as err:
            return {"message": f"Failed to read encryption key\n{type(err).__name__}: {err}", "status": 400}
        
    def create_key(self):
        # Use string and secrets to generate a 16 character passphrase
        alphanums = string.ascii_letters + string.digits
        passphrase = ''.join(secrets.choice(alphanums) for _ in range(128))

        try:
            # Create key file
            with open("SSO/backend/utils/.key.txt", "w") as f:
                f.write(passphrase)
            return {"message": "Key created!", "status": 200}
        except Exception as err:
            return {"message": f"Failed to create key\n{type(err).__name__}: {err}", "status": 400}

    # Creates credentials table and returns the output
    def create_credentials(self):
        try:
            self.database.fullrun(
                """
                CREATE TABLE credentials (
                    username varchar(30) PRIMARY KEY,
                    password varbinary(255) NOT NULL
                )
                """
            )
            return {"message": "credentials table created!", "status": 200}
        except Exception as err:
            return {"message": f"Failed to create credentials table\n{type(err).__name__}: {err}", "status": 400}

    def create_user(self, username, password):

        # Check if the user already exists in the database
        if self.database.run(f"SELECT * FROM credentials WHERE username='{username}'") != ():
            return {"message": "Username already exists in database.", "status": 400}
        
        # Insert the username and password, using AES encryption on the password
        if self.database.run(f"INSERT INTO credentials VALUES ('{username}', AES_ENCRYPT('{password}', '{self.key}'))") == ():
            self.create_profile(username)
            return {'message': 'Successfully created user', 'status': 200}
        else:
            return {'message': 'Failed to create user', 'status': 400}

    
    # Commit changes to the database
    def save(self):
        self.database.commit()

    # Verify a user by username and password
    def verify_user(self, username, password):
        try:
            # Retrieve decrypted password from credentials
            decrypted = self.database.run(f"SELECT AES_DECRYPT(password, '{self.key}') FROM credentials WHERE username='{username}'")
            if password == decrypted[0][0].decode('ASCII'):
                if self.load_profile(username):
                    return {"message": "Login Successful, Profile Loaded", "status": 200}
                else:
                    return {"message": "Login Successful, Failed to Load Profile", "status": 400}
            else:
                return {"message": "Incorrect password.", "status": 400}
        except (IndexError, TypeError):
            return {"message": "Username does not exist.", "status": 400}
        except Exception as err:
            return {"message": f"{type(err).__name__} {err}", "status": 500}
        
    def create_profile(self, username):
        # Create a default profile based on the username and default profile picture
        return self.database.fullrun(f"""
            INSERT INTO users VALUES (
                "{username}",
                "{username}",
                "Default profile picture file path",
                " "
            );
        """)
        
    def load_profile(self, username):
        # Load the user information into the profile info for formatting
        profile_info = self.database.fullrun(f"""
            SELECT display_name, profile_picture, bio
            FROM users
            WHERE username='{username}'
        """)

        # Unpack table output
        display_name, profile_picture, bio = profile_info[0][0]

        # Store formatted data in profile_info
        self.profile_info = {
            'display_name': display_name,
            'profile_picture': profile_picture,
            'bio': bio
        }

        return True


        

    def delete_user(self, username):
        self.database.run(f"DELETE FROM credentials WHERE username='{username}'") # Delete login info
        self.database.run(f"DELETE FROM users WHERE username='{username}'")       # Delete profile