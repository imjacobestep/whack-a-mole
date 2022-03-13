import pyodbc

server = 'whack-a-mole.database.windows.net'
database = 'sessions_db'
username = 'whackamole'
password = 'password123!'
driver = '{ODBC Driver 13 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()