import datetime
from Azure.Database import Database

database = Database()
database.connect()

timeStamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
msg = "'{}',{}".format(timeStamp,  "1,1,1,1,1,1")
# print(msg)

database.insert(msg)

database.select()
