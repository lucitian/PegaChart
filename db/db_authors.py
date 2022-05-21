from .db_backbone import DatabaseBackbone
from secret import CONN_STRING

class AuthorsBackbone(DatabaseBackbone):
    def __init__(self):
        self.conn_string = CONN_STRING
    
    def add_author(self, rid, research_id, author_type):
        try:
            self.append_row(
                "research_authors",
                research_id = research_id,
                user_id = rid,
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