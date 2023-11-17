import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')

waterDB = client['water']
nitrate = waterDB['nitrate']

# nitrate.drop()
# rand = [random.gauss() for _ in range(10_000)]
# nitrate.insert_many([{'value': r} for r in rand])

# print(list(nitrate.aggregate([{'$group': {'_id': None, 'avgValue': {'$avg': '$value'}}}])))
# print(statistics.mean(rand))

print(list(nitrate.find()))