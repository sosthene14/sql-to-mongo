import random

from pymongo import MongoClient
from bson import ObjectId
import datetime
import uuid

client = MongoClient('mongodb://127.0.0.1', 27017)
db = client['modeles_version_mongo']

test = db["test"]
region = db["region"]
departement = db['departement']
commune = db['commune']
localite = db['localite']
ouvrage = db['ouvrage']
sigautonome_site = db['sigautonome_site']


def insert_region():
    print("loading ...")
    objet = {
        "code": "XX",
        "libelle": "Region Name"
    }
    result = region.insert_one(objet)
    print("inserted region")
    return insert_departement(result.inserted_id)


def insert_departement(region_id):
    objet = {
        "libelle": "Department Name",
        "region_id": region_id
    }
    result = departement.insert_one(objet)
    print("inserted departement")
    return insert_commune(result.inserted_id)


def insert_commune(departement_id):
    objet = {
        "libelle": "Commune Name",
        "departement_id": departement_id
    }
    result = commune.insert_one(objet)
    print("inserted commune")
    return insert_localite(result.inserted_id)


def generate_random_id():
    return str(uuid.uuid4())


def insert_localite(commune_id):
    objet = {
        "libelle": "Localite Name",
        "type_ouvrage": "Type Ouvrage",
        "commune_id": commune_id
    }
    random_society_id = generate_random_id()
    result = localite.insert_one(objet)
    print("inserted locality")
    return insert_ouvrage(random_society_id, result.inserted_id)


def insert_ouvrage(entreprise_id, localite_id):
    objet = {
        "type_ouvrage": "Type Ouvrage",
        "connectivite": "Connectivite",
        "type_sol": "Type Sol",
        "bailleur": "Bailleur",
        "etat_ouvrage": "Etat Ouvrage",
        "date_reception": datetime.datetime.now(datetime.timezone.utc),
        "entreprise_id": entreprise_id,
        "localite_id": localite_id
    }

    ouvrage.insert_one(objet)
    print("inserted ouvrage")
    return sigautonome_site_(entreprise_id, localite_id)


def sigautonome_site_(entreprise_id, localite_id):
    objet = {
        "libelle": "Site Name",
        "date_reception": datetime.datetime.now(datetime.timezone.utc),
        "entreprise_id": entreprise_id,
        "localite_id": localite_id
    }
    print("inserted sigautonome")
    sigautonome_site.insert_one(objet)


if __name__ == "__main__":
    print("oo")
    insert_region()
