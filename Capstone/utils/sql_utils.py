import mysql.connector
from mysql.connector import Error
from mysql.connector.types import RowType

# Prompt user and validate input
def prompt(text: str, options: tuple[str]) -> str:

    ans = input(f"{text} {options}")

    while ans not in options:
        ans = input(f"Please choose a valid option: {options}")

    return ans

# Safe connection and cursor querying
class SafeSQL:
    
    def __init__(self, user: str, password: str, host: str, database: str, *, verbose: bool = False) -> None:

        self.verbose = verbose
        
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
    def run(self, query: str) -> list[RowType]:

        try:
            # Execute query and increment query count
            self.cursor.execute(query)
            self.query_count += 1
            
            # Return query results
            output = self.cursor.fetchall()

            if self.verbose:
                print(f"{output}\n{self.cursor.rowcount} row(s) affected.")

            return output

        except Error as err:

            print(f"Failed to execute: '{query}'\nError: {err}")
            self.error_count += 1

            return None

    # Takes a multi-line query, returns a list of outputs
    def fullrun(self, multiquery: str) -> list[list[RowType]]:
        
        # Initialize output list
        outputs = []
        
        # Filter out whitespace and newlines, extract list of query strings
        query_arr = [q.strip() for q in multiquery.split(';') if q.strip()]

        # Run each query and append the result to the outputs
        for query in query_arr:
            outputs.append(self.run(query))

        if self.verbose:
            print(f"Executed {len(query_arr)} queries.")

        return outputs
    
    # Runs an sql file and returns the output
    def run_file(self, sql_file: str) -> list[list[RowType]]:

        # Read file contents
        with open(sql_file, 'r') as f:
            contents = f.read()

        # Execute queries and return the outputs
        return self.fullrun(contents)


    # Safe commit function
    def commit(self) -> None:

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

    # Close the cursor and connection
    def close(self) -> None:

        print("Closing connection...")

        self.cursor.close()
        self.connector.close()