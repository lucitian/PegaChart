from urllib.request import urlopen
from pymongo import MongoClient
from secret import DB_KEY
import json

class Pega:
    def __init__(self, pega_id):
        self.pega_id = int(pega_id)
        cluster = MongoClient(DB_KEY)
        db = cluster['racesDB']
        collection = db['race_history']

        self.db = collection 

    
    @property 
    def exists(self):
        try:
            data = urlopen(f'https://api-apollo.pegaxy.io/v1/game-api/pega/{self.pega_id}')

            if data.read() == b'"Not Found"':
                return False 
            else:
                return True
        except:
            return False
    
    @property 
    def in_database(self):
        if len(list(self.db.find({'pega_id': self.pega_id}))) == 0:
            return False 
        else:
            return True
    
    @property 
    def name(self):
        data = urlopen(f'https://api-apollo.pegaxy.io/v1/game-api/pega/{self.pega_id}')

        data_json = json.loads(data.read())['pega']

        return data_json['name']
    
    @property 
    def win_rate(self):
        data = urlopen(f'https://api-apollo.pegaxy.io/v1/game-api/pega/{self.pega_id}')

        data_json = json.loads(data.read())['pega']

        return data_json['win'] / data_json['total_races']
    
    @property 
    def race_history(self):
        data = list(self.db.find({'pega_id': self.pega_id}))[0]
        print(data['races'])
    
    def add_pega(self, pega):
        self.db.insert_one(pega)