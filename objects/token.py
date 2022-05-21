from db import db_token

class Token:
    def __init__(self, token = None):
        self.token = token
        self.db = db_token.TokenBackbone()
    
    @property
    def is_expired(self):
        return self.db.token_expired(self.token)
    
    def expire_token(self, token):
        return self.db.expire_token(token)