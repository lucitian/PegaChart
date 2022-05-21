from secret import MONGO_CONN_STRING, MONGO_DB, MONGO_STUDY_COLLECTION
from pymongo import MongoClient
from bson.objectid import ObjectId

class StudiesBackbone():
    def __init__(self):
        self.db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_STUDY_COLLECTION]
    
    def new_study(self, **kwargs):
        try:
            self.db.insert_one({
                'study_name': kwargs['study_name'],
                'study_description': kwargs['study_description'],
                'research_id': ObjectId(kwargs['research_id']),
                'created_by': ObjectId(kwargs['created_by']),
                'test_type': kwargs['test_type'],
                'study_dataset': kwargs['study_dataset'],
                'interpretations': kwargs['interpretations'],
                'columns': kwargs['columns'],
                'variables': kwargs['variables'],
                'options': kwargs['options'],
                'changes': kwargs['changes'],
                'configurations': kwargs['regression_configuration'],
                'created_at': kwargs['created_at'],
                'graphing': kwargs['graphing']
            })

            return {
                'status': True
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def is_registered(self, uid):
        try:
            fetched = self.db.find_one({
                '_id': ObjectId(uid)
            })
            
            return False if fetched is None else True
        except Exception as e :
            return {
                'status': False,
                'message': str(e)
            }
    
    def get_study(self, uid):
        try: 
            study = self.db.find_one({
                '_id': ObjectId(uid)
            })

            return study
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def delete_study(self, rid):
        try:
            self.db.delete_one({
                '_id': ObjectId(rid)
            })

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }