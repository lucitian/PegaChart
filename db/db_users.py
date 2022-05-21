from secret import MONGO_CONN_STRING, MONGO_DB, MONGO_USER_COLLECTION, MONGO_RESEARCH_COLLECTION
from pymongo import MongoClient
from bson.objectid import ObjectId

class UsersBackbone():
    def __init__(self):
        self.db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_USER_COLLECTION]
        self.research_db = MongoClient(MONGO_CONN_STRING)[MONGO_DB][MONGO_RESEARCH_COLLECTION]

    def register_user(self, **kwargs):
        try:
            self.db.insert_one({
                'first_name': kwargs['first_name'],
                'middle_name': kwargs['middle_name'],
                'last_name': kwargs['last_name'],
                'username': kwargs['username'],
                'password_hash': kwargs['password_hash'],
                'email_address': kwargs['email_address'],
                'nickname': kwargs['nickname'],
                'educ_level': kwargs['educ_level'],
                'major': kwargs['major'],
                'occupation': kwargs['occupation'],
                'profile_picture': kwargs['profile_picture'],
                'bio': kwargs['bio'],
                'created_at': kwargs['created_at']
            })

            return {
                'status': True, 
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def is_registered(self, uid):
        try:
            if len(uid) < 12: 
                return False 
                
            fetched = self.db.find_one({
                '_id': ObjectId(uid)
            })
            
            return False if fetched is None else True
        except Exception as e :
            return {
                'status': False,
                'message': str(e)
            }
    
    def check_email_availability(self, email):
        try:
            fetched = self.db.find_one({
                'email_address': email
            })

            return True if fetched is None else 'EMAIL_TAKEN'
        except Exception as e :
            return {
                'status': False,
                'message': str(e)
            }
    
    def check_username_availability(self, uname):
        try:
            fetched = self.db.find_one({
                'username': uname
            })

            return True if fetched is None else 'USERNAME_TAKEN'
        except Exception as e :
            return {
                'status': False,
                'message': str(e)
            }

    def get_user(self, uid):
        try: 
            user = self.db.find_one({
                '_id': ObjectId(uid)
            })

            user.pop('password_hash')

            user['_id'] = str(user['_id'])

            return user
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def login_credentials(self, uname):
        try: 
            user = self.db.find_one({
                'username': uname
            })

            if user is None:
                return None

            return {'_id': str(user['_id']), 'username': user['username'], 'password_hash': user['password_hash']}
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def get_researches(self, uid):
        try: 
            data = []
            researches = self.research_db.find({
                'authors': {'$elemMatch': {'user': ObjectId(uid)}}
            })

            for research in researches: 
                research['_id'] = str(research['_id'])
                data.append({
                    '_id': research['_id'],
                    'research_name': research['research_name'],
                    'research_description': research['research_description'],
                    'created_at': research['created_at']
                })

            return data
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
    
    def set_first_name(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'first_name': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_middle_name(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'middle_name': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_last_name(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'last_name': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_username(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'username': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_password_hash(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'password_hash': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_email_address(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'email_address': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_nickname(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'nickname': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_educ_level(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'educ_level': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_major(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'major': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
            
    def set_occupation(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'occupation': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_profile_picture(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'profile_picture': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    def set_bio(self, uid, new):
        try:
            self.db.update_one({'_id': ObjectId(uid)}, {'$set': {'bio': new}})

            return True
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }