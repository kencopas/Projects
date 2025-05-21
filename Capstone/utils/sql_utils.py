import mysql.connector
from mysql.connector import Error
from mysql.connector.types import RowType
import json

# Prompt user and validate input
def prompt(text: str, options: tuple[str]) -> str:

    ans = input(f"{text} {options}")

    while ans not in options:
        ans = input(f"Please choose a valid option: {options}")

    return ans

# Safe connection and cursor querying
class SafeSQL:

    """
    
    This class just simplifies MySQL operations with error handling and configuration.
    
    """
    
    def __init__(self, **kwargs) -> None:

        self.verbose = kwargs.pop('verbose', False)
        
        # Attempt to connect to mysql local instance
        try:
            print(kwargs)
            self.connector = mysql.connector.connect(**kwargs)
        except Error as err:
            print("Could not connect to server:", err)
            exit()

        # Initialize cursor
        self.cursor = self.connector.cursor()
        
        # Tracks error count and query count
        self.error_count = 0
        self.query_count = 0

    # Safe query function, takes an sql script as text or a filepath, executes the contents, and returns a list of the results
    def run(self, sqlin: str) -> list[RowType] | list[list[RowType]]:

        try:
            # Initialize list of outputs
            outputs = []
            rowcount = 0

            # If a filepath is passed, read the file contents into the content variable
            if len(sqlin) >= 4 and sqlin[-4:] == ".sql":
                # Read file contents
                with open(sqlin, 'r') as f:
                    content = f.read()
            # Otherwise, assign the sqlin to content
            else:
                content = sqlin

            # If multiple queries are passed, filter out whitespace and newlines, extract list of query strings
            query_arr = [q.strip() for q in content.split(';') if q.strip()]

            # Run each query and append the result to the outputs
            for query in query_arr:

                # Execute query and increment query count
                self.cursor.execute(query)
                self.query_count += 1
                rowcount += self.cursor.rowcount
                
                # Append the query results to outputs
                outputs.append(self.cursor.fetchall())

            if self.verbose:
                print(f"Executed {len(query_arr)} queries.\n{rowcount} rows affected.")

            # Returns the list of outputs if multi-query, otherwise unpack and return
            return outputs if len(outputs) > 1 else outputs[0]

        except Error as err:

            print(f"Failed to execute: '{sqlin}'\nError: {err}")
            self.error_count += 1

            return None

    # Safe commit function
    def commit(self) -> None:

        # If there are one or more errors, prompt the user before committing
        if self.error_count > 0:
            ans = input(f"{self.error_count} errors occured during query. Would you still like to commit?  Y | N \n")
            if ans.lower() != "y":
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

if __name__ == "__main__":

    with open("config.json", 'r') as f:
        data = json.load(f)

    ssql = SafeSQL(
        user=data['user'],
        password=data['password'],
        host=data['host'],
        database='classicmodels',
        verbose=True
    )

    for row in ssql.run("init.sql"):
        print(row)