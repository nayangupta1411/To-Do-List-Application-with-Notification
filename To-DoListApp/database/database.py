from pymongo import MongoClient 

DATABASE_BASE='mongodb://localhost:27017/'
print('database--',DATABASE_BASE)

client=MongoClient("mongodb://localhost:27017/")
todoAppDB=client['todoAppDB']

# todoAppDB_collection=todoAppDB.create_collection('task')
# todoAppDB_collection.insert_one({
#     'inputTaskName':'Assignment',
#     'inputTaskDescription':'mini project task',
#     'inputDate':'2024-11-18',
#     'inputTime': '16:35',
#     'inputCategory':'Default'
# })


print('client-',client.list_database_names())
db=client.todoAppDB