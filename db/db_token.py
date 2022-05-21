from .db_backbone import DatabaseBackbone
from secret import MONGO_CONN_STRING, MONGO_DB, MONGO_TOKEN_COLLECTION
from pymongo import MongoClient

class TokenBackbone():
    def __init__(self):
        self.db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_TOKEN_COLLECTION]
    
    def token_expired(self, token):
        try:
            fetched = self.db.find_one({
                'token': str(token) 
            })

            return True if fetched else False
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def expire_token(self, token):
        try:
            self.db.insert_one({
                'token': str(token)
            })

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }