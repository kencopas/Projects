"""

This program pulls medical records from an API endpoint and loads them into
memory. The data that is extracted and saved is all temperatures recorded
partitioned by doctor name and diagnosis id. For efficient lookup, this
information is stored in a dictionary that holds a tuple key
(doctor_name, diagnosis_id) and a list value [temp1, temp2, temp3...]. Upon
user query, this information is retrieved in O(1) time and the maximum and
minimum temperature values are retreived in O(n) time.

"""

import requests

# Initialize a dictionary with the format (doctor_name, diagnosis_id):
# [temp1, temp2, temp3...]
temperatures = {}


# Extract the medical records, transform them to be accessed by doctor name
# and diagnosis id, and store the data in the temperatures dictionary
def etl():
    # Initialize index
    n = 1
    # Traverse the pages, adding each data set to the records
    while True:
        # Set the url to the current page referencing n as the page number
        url = f"https://jsonmock.hackerrank.com/api/medical_records?page={n}"

        # Attempt to fetch the data from the url
        try:
            # Retrieve the data, parse it into json
            data = requests.get(url).json()

            # Iterate through each record in the list of data
            for record in data['data']:
                # Extract the doctor name, diagnosis id, and bodyTemperature
                doctor_name = record['doctor']['name'].lower()
                diagnosis_id = record['diagnosis']['id']
                temperature = record['vitals']['bodyTemperature']

                # Create a tuple key for the temperature dictionary
                key = (doctor_name, diagnosis_id)
                
                # If the key does not exist in the dictionary, create an empty
                # list with that key
                if not temperatures.get(key):
                    temperatures[key] = []
                
                # Append the temperature to the list
                temperatures[key].append(temperature)

        # Catch any exception, print it to the console, break
        except Exception as err:
            # Format -> [Exception Name]: [Exception]
            print(f"{type(err).__name__}: {err}")
            break
        
        # Break if the page limit is hit
        if n >= data["total_pages"]:
            break

        # Otherwise increment n
        n += 1

    print("Data successfully loaded.")

# Reference the temperatures dictionary by key (doctor_name, diagnosis_id) to
# retrieve the list of temperatures. Return the max and min temperature
def body_temperature(doctor_name, diagnosis_id):

    # If the temperatures have not been pulled from the api, call etl
    if not temperatures:
        etl()

    # Retrieve the list of temperatures by doctor name and diagnosis id
    temps = temperatures.get((doctor_name.lower(), diagnosis_id))

    # Return [None, None] if the doctor name and diagnosis id did not match any records
    if not temps:
        return [None, None]
    
    # Otherwise, return the minimum and maximum temperature from the records, truncated
    return [int(min(temps)), int(max(temps))]

# ------------------------------ TEST CASES ------------------------------ #

if __name__ == "__main__":

    etl() # Load the data first

    test_inputs = [("Dr Arnold Bullock", 3), ("Dr Allysa Ellis", 4), ("Dr Adam", 5)]

    for i, test_input in enumerate(test_inputs):

        print(f"\nTest Case {i+1}")

        doctor_name, diagnosis_id = test_input
        result = body_temperature(doctor_name, diagnosis_id)
        print("Minimum Body Temperature:", result[0])
        print("Maximum Body Temperature:", result[1])