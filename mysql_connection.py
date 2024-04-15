import mysql.connector

mydb_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Rk@9709648171",
  database="flask-signup-login"
)

print(mydb_connection, " this is db connection object.........................................")

mycursor = mydb_connection.cursor()

# mycursor.execute("CREATE TABLE signup_table (email VARCHAR(25),username VARCHAR(20), password VARCHAR(12))")