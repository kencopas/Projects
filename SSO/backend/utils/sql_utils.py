import mysql.connector
from mysql.connector import Error

# Prompt user and validate input
def prompt(text: str, options: tuple) -> str:
    ans = input(f"{text} {options}")
    while ans not in options:
        ans = input(f"Please choose a valid option: {options}")
    return ans

# Safe connection and cursor querying
class safe_connect:

    """
    
    This class creates a mysql connector and cursor. You can call cursor methods directly and safely, and pass multi-line queries with the fullrun method.
    
    """

    def __init__(self, user: str, password: str, host: str, database: str):

        self.verbose = False
        
        # Attempt to connect to mysql local instance
        try:
            self.connector = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except Error as err:
            print("Could not connect to server:", err)
            exit()

        # Initialize cursor
        self.cursor = self.connector.cursor()
        
        # Tracks error count and query count
        self.error_count = 0
        self.query_count = 0

    # Safe query function, prints and returns the result. Returns false if the statement results in an error
    def run(self, query, error_message=""):

        try:
            # Execute query and increment query count
            self.cursor.execute(query)
            self.query_count += 1
            
            # Return query results
            output = self.cursor.fetchall()
            if self.verbose: print(f"{output}\n{self.cursor.rowcount} row(s) affected.")
            return output

        except Error as err:
            # Print error and increment error count
            print(error_message)
            if self.verbose: print(f"Failed to execute: '{query}'\nError: {err}")
            self.error_count += 1
            return False

    # Takes a multi-line query, returns a list of outputs
    def fullrun(self, multiquery: str):
        
        # Initialize output list
        outputs = []
        
        # Filter out whitespace and newlines, extract list of query strings
        query_arr = [q.strip() for q in multiquery.split(';') if q.strip()]

        # Run each query and append the result to the outputs
        for query in query_arr:
            outputs.append(self.run(query))

        return outputs

    # Safe commit function
    def commit(self):

        # If there are one or more errors, prompt the user before committing
        if self.error_count > 0:
            ans = input(f"{self.error_count} errors occured during query. Would you still like to commit?  Y | N \n")
            if ans != "Y":
                print("Commit aborted.")
                return
            
        self.connector.commit()
        print(self.query_count, "queries committed.")

        # Reset error and query counters
        self.error_count, self.query_count = 0, 0

    def close(self):
        self.cursor.close()
        self.connector.close()

if __name__ == "__main__":
    
    # Create a safe connection to database
    scnx = safe_connect(user='root', password='password', host='127.0.0.1', database='data')

    # Run a multi-line query
    print(scnx.fullrun("""
                   SELECT * FROM credentials;
                   SELECT username FROM credentials;
                   """))

    # Close the connection
    scnx.close()