from random import randint
from db import db_users
from db import db_authors
import jwt, datetime, bcrypt

class User:
    def __init__(self, uid = None):
        self.db = db_users.UsersBackbone()
        self.rdb = db_authors.AuthorsBackbone()
        self.uid = uid
    
    @property 
    def is_registered(self):
        return self.db.is_registered(self.uid)
    
    @property 
    def research_papers(self):
        return self.db.get_researches(self.uid)
    
    def get_user(self):
        return self.db.get_user(self.uid)
    
    def set_first_name(self, new_first_name):
        return self.db.set_first_name(self.uid, new_first_name)
    
    def set_middle_name(self, new_middle_name):
        return self.db.set_middle_name(self.uid, new_middle_name)
    
    def set_last_name(self, new_last_name):
        return self.db.set_last_name(self.uid, new_last_name)
    
    def set_username(self, new_username):
        return self.db.set_username(self.uid, new_username)
    
    def set_password_hash(self, new_password_hash):
        return self.db.set_password_hash(self.uid, new_password_hash)
    
    def set_email_address(self, new_email_address):
        return self.db.set_email_address(self.uid, new_email_address)
    
    def set_nickname(self, new_nickname):
        return self.db.set_nickname(self.uid, new_nickname)
    
    def set_educ_level(self, new_educ_level):
        return self.db.set_educ_level(self.uid, new_educ_level)
    
    def set_major(self, new_major):
        return self.db.set_major(self.uid, new_major)
    
    def set_occupation(self, new_occupation):
        return self.db.set_occupation(self.uid, new_occupation)
    
    def set_profile_picture(self, new_profile_picture):
        return self.db.set_profile_picture(self.uid, new_profile_picture)
    
    def set_bio(self, new_bio):
        return self.db.set_bio(self.uid, new_bio)
    
    def check_email_availability(email):
        db = db_users.UsersBackbone()
        
        return db.check_email_availability(email)

    def check_username_availability(uname):
        db = db_users.UsersBackbone()
        
        return db.check_username_availability(uname)
    
    def register_user(**kwargs):
        db = db_users.UsersBackbone()

        return db.register_user(
                first_name = kwargs['first_name'],
                middle_name = kwargs['middle_name'],
                last_name = kwargs['last_name'],
                username = kwargs['username'],
                password_hash = kwargs['password_hash'],
                email_address = kwargs['email_address'],
                nickname = kwargs['nickname'], 
                educ_level = kwargs['educ_level'], 
                major = kwargs['major'],
                occupation = kwargs['occupation'],
                profile_picture = kwargs['profile_picture'],
                bio = kwargs['bio'],
                created_at = kwargs['created_at']
            )
    
    def authenticate(username, password, secret_key):
        db = db_users.UsersBackbone()

        user = db.login_credentials(username)

        if user is None:
            return False, "Username does not match any account.", None

        pword = user['password_hash']

        if not bcrypt.checkpw(password.encode('utf-8'), pword.encode('utf-8')):
            return False, "Credentials failed to authenticate.", None
        
        try:
            payload = {
                'flush': randint(10000000, 99999999),
                'sub': user['_id']
            } 
                                
            token = jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return False, f"Token generation failed returning with error message: {e}.", None
        
        return True, user['_id'], token
    
    @staticmethod
    def decode_auth_token(auth_token, secret_key):
        try:
            payload = jwt.decode(auth_token, secret_key, ['HS256'])

            return payload['sub']
        except jwt.ExpiredSignatureError:
            return {'error': 'Token already expired.'}
        except jwt.InvalidTokenError:
            return {'error': f'Token is not valid. Token value: {auth_token}'}
        except Exception as e:
            raise e