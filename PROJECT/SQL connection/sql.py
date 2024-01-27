import psycopg2
from pw import password
# Use your actual password here

password = password
# Establish a connection to the database
conn = psycopg2.connect(
    dbname="PROJECT",
    user="postgres",
    password=password,
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Execute a query to select all rows from the 'dim_wh' table
cur.execute("SELECT * FROM SEB LIMIT 10;")

# Fetch and print the first row
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()
