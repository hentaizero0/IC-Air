
# Setup Instruction: http://mdupont.com/Blog/Raspberry-Pi/azure-python3.html

import pyodbc

class Database:
    pass
    def __init__(self):
        self._server = 'test-database.database.windows.net'
        self._database = 'test-database'
        self._username = 'test'
        self._password = 'qwer1234!'
        self._driver= 'FreeTDS'
        self._connection = None
        self._cursor = None
    # end

    def connect(self):
        self._connection = pyodbc.connect('DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version=8.0'.format(self._driver, self._server, self._database, self._username, self._password))
        self._cursor = self._connection.cursor()
    # end

    def insert(self, data):
        self._cursor.execute("INSERT INTO dbo.EnvData VALUES ({})".format(data))
    # end
# end
