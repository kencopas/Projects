import requests
from sql_utils import safe_connect
from googletrans import Translator
import asyncio

# Safely retreive a response from an endpoint
def fetch_posts(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Failed to fetch data. Status code: {response.status_code}")

def load_to_mysql(data):
    
    # Establish a Safe Connection to the classicmodels database
    sc = safe_connect(host='localhost', user='root', password='password', database='classicmodels')
    sc.verbose = True
    
    # Create the posts table if it does not exist
    sc.run("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT PRIMARY KEY,
            userId INT,
            title VARCHAR(255),
            body TEXT
        )
    """)

    # Insert the data into the table
    for post in data:
        sc.run(f"""
            INSERT INTO posts
                (id, userId, title, body)
            VALUES
                ({post['id']}, {post['userId']}, '{post['title']}', '{post['body']}')
        """)
    
    # Safe Commit changes
    sc.commit()

# Fetch all loaded information from classicmodels database
def fetch_from_mysql():
    
    # Establish a Safe Connection to the classicmodels database
    sc = safe_connect(host='localhost', user='root', password='password', database='classicmodels')

    # Retrieve all records from the posts table
    records = sc.run("SELECT * FROM posts")

    print("Total number of rows in table:", sc.cursor.rowcount)
    print("\nPrinting each row")
    
    # Print each row
    for row in records:
        print("order number = ", row[0], )
        print("item counts = ", row[1])
        print("total = ", row[2], "\n" )

data = fetch_posts(r'https://jsonplaceholder.typicode.com/posts/')

# Translates all of the text from each post from latin to english
async def translate_all():
    async with Translator() as t:
        for post in data:
            res = await t.translate(post['body'])
            print(res.text)

if data:
    load_to_mysql(data)          # Load all fetched data to mysql
    fetch_from_mysql()           # Fetch data from mysql
    asyncio.run(translate_all()) # Translate all data's body text to english