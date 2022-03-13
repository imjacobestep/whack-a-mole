import pymssql

server = 'whack-a-mole.database.windows.net'
database = 'sessions_db'
username = 'whackamole'
password = 'password123!'
driver = 'FreeTDS'
#driver = '/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so'
userID = "Test2"
#connection = pymssql.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
#connection = pymssql.connect(server, username, password, database)
pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password + ';TDS_Version=8.0')

cursor = connection.cursor(as_dict=True)

queryVals = f"VALUES({userID})"
cursor.execute(f"INSERT INTO sessions (user_id, avg_reaction, mole_score, mem_1_score, mem_2_score, mem_3_score, hr_data) {queryVals}")
