from .db_backbone import DatabaseBackbone
from secret import CONN_STRING
from secret import MONGO_CONN_STRING, MONGO_DB, MONGO_RESEARCH_COLLECTION, MONGO_STUDY_COLLECTION
from pymongo import MongoClient
from bson.objectid import ObjectId

class ResearchesBackbone(DatabaseBackbone):
    def __init__(self):
        self.conn_string = CONN_STRING
        self.db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_RESEARCH_COLLECTION]
        self.studies_db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_STUDY_COLLECTION]
    
    def register_research(self, **kwargs):
        try:
            res = self.db.insert_one({
                'research_name': kwargs['research_name'], 
                'research_description': kwargs['research_description'],
                'dataset': kwargs['dataset'],
                'dataset_details': kwargs['dataset_details'],
                'authors': [{
                    'user': ObjectId(kwargs['author']),
                    'type': 'OWNER' 
                }],
                'delimiter': kwargs['delimiter'],
                'created_at': kwargs['created_at']
            })

            return {
                'status': True, 
                '_id': str(res.inserted_id)
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
        
    def is_registered(self, rid):
        try:
            if len(rid) < 24:
                return False 
                
            fetched = self.db.find_one({
                '_id': ObjectId(rid)
            })
            
            return False if fetched is None else True
        except Exception as e :
            return {
                'status': False,
                'message': str(e)
            }
    
    def get_research(self, rid):
        try:
            research = self.db.find_one({
                '_id': ObjectId(rid)
            })

            research['_id'] = str(research['_id'])

            for author in research['authors']:
                author['user'] = str(author['user'])
           
            return research
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def get_studies(self, rid):
        try:
            studies = self.studies_db.find({
                'research_id': ObjectId(rid)
            })
            
            temp = []

            for study in studies:
                study['_id'] = str(study['_id'])
                study['created_by'] = str(study['created_by'])
                study['research_id'] = str(study['research_id'])
                temp.append(study)
           
            return temp
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_research_name(self, rid, new):
        try:
            self.update_data(
                "researches",
                "research_name",
                new,
                _id = rid
            )

            return True
        except Exception as e:
            print(e)
            return False

    def set_research_description(self, rid, new):
        try:
            self.update_data(
                "researches",
                "research_description",
                new,
                _id = rid
            )

            return True
        except Exception as e:
            print(e)
            return False

    def set_dataset(self, rid, new):
        try:
            self.update_data(
                "researches",
                "dataset",
                new,
                _id = rid
            )

            return True
        except Exception as e:
            print(e)
            return False

    def set_test_type(self, rid, new):
        try:
            self.update_data(
                "researches",
                "test_type",
                new,
                _id = rid
            )

            return True
        except Exception as e:
            print(e)
            return False
    
    def set_delimiter(self, rid, new):
        try:
            self.update_data(
                "researches",
                "delimiter",
                new,
                _id = rid
            )

            return True
        except Exception as e:
            print(e)
            return False
    
    def add_author(self, uid, research_id, author_type):
        try:
            self.append_row(
                "research_authors",
                research_id = research_id,
                user_id = uid,
                author_type = author_type
            )

            return True
        except Exception as e:
            print(e)
            return False
    
    def get_researches_author(self, rid):
        try:
            fetched = self.fetch_row(
                "research_authors",
                user_id = rid
            )

            data = [i[0] for i in fetched]

            return data
        except Exception as e:
            print(e)
            return False
    
    def get_authors(self, rid):
        try:
            fetched = self.fetch_row(
                "research_authors",
                research_id = rid
            )

            data = [i[1] for i in fetched]

            return data
        except Exception as e:
            print(e)
            return False
    
    def delete_research(self, rid):
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