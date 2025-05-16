from sql_utils import safe_connect

# Establish a Safe Connection to the mysql database
sc = safe_connect(database='usersdb', user='root', password='password', host='localhost')
sc.verbose = True

# Create the table
def create_table():
    sc.fullrun("""
        CREATE TABLE laptop (
            Id int(11) NOT NULL, 
            Name varchar(250) NOT NULL,
            Price float NOT NULL,
            Purchase_date date NOT NULL
            )
    """)

def insert_values(id, name, price, purchase_date):
    sc.fullrun(f"""
        INSERT INTO laptop 
            (Id, Name, Price, Purchase_date)
        VALUES
            ({id}, '{name}', {price}, '{purchase_date}')
    """)

def execute_many(func, args):
    for arg_set in args:
        func(*arg_set)

# Insert values into table
insert_values(15, 'Lenovo ThinkPad P71', 6459, '2019-08-14')
insert_values(2, 'Area 51M', 6999, '2019-04-14')
insert_values(3, 'MacBook Pro', 2499, '2019-06-20')

# Execute many function
execute_many(insert_values, [(15, 'Lenovo ThinkPad P71', 6459, '2019-08-14'),
                             (2, 'Area 51M', 6999, '2019-04-14'),
                             (3, 'MacBook Pro', 2499, '2019-06-20')])

# Safe Commit all changes to the database
sc.commit()