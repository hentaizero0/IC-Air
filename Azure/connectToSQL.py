
# Setup Instruction: http://mdupont.com/Blog/Raspberry-Pi/azure-python3.html

import pyodbc
server = 'test-database.database.windows.net'
database = 'test-database'
username = 'test'
password = 'qwer1234!'
driver= 'FreeTDS'

with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';TDS_Version=8.0') as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 id, val FROM dbo.Test")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
        # end
    # end
# end
