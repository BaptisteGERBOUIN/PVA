from pymongo import MongoClient

# Spécifiez l'URL de connexion à MongoDB
# L'URL doit suivre le format mongodb://<nom_utilisateur>:<mot_de_passe>@<hôte>:<port>/<nom_base_de_données>
url = "mongodb://localhost:27017/ma_base_de_donnees"

# Initialisez une instance MongoClient
client = MongoClient(url)

# Sélectionnez la base de données
db = client.ma_base_de_donnees

# Accédez à une collection
collection = db.ma_collection

print()

# Maintenant, vous pouvez interagir avec la collection, par exemple :
# collection.insert_one({"nom": "John", "age": 30})

