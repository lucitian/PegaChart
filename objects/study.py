from db import db_studies

class Study:
    def __init__(self, study_id):
        self.db = db_studies.StudiesBackbone()
        self.id = study_id 
    
    @property
    def is_registered(self):
        return self.db.is_registered(self.id)

    @property
    def name(self):
        return self.db.get_study_name(self.id)
    
    @property
    def description(self):
        return self.db.get_study_description(self.id)
    
    @property 
    def research_parent(self):
        return self.db.get_research_id(self.id)
    
    @property 
    def author(self):
        return self.db.get_author(self.id)
    
    @property 
    def test_type(self):
        return self.db.get_test_type(self.id)
    
    @property 
    def created_at(self):
        return self.db.get_created_at(self.id) 
    
    @property 
    def columns(self):
        return self.db.get_columns(self.id)
    
    @property
    def variables(self):
        return self.db.get_variables(self.id)
    
    @property
    def regression_configuration(self):
        return self.db.get_regression_configuration(self.id)
    
    def get_study(self):
        return self.db.get_study(self.id)

    def clean_stats(self, column):
        return self.db.get_clean_stats(self.id, column)
    
    def set_study_name(self, name):
        return self.db.set_study_name(self.id, name)
    
    def add_column(self, column):
        return self.db.add_column(self.id, column)
    
    def add_regression_configuration(self, test_size, iterations, learning_rate):
        return self.db.add_regression_configuration(self.id, test_size, iterations, learning_rate)
    
    @staticmethod
    def new_study(**kwargs):
        db = db_studies.StudiesBackbone()
        return db.new_study(
            _id = kwargs['_id'],
            study_name = kwargs['study_name'],
            research_id = kwargs['research_id'],
            created_by = kwargs['created_by'],
            test_type = kwargs['test_type'],
            study_dataset = kwargs['study_dataset'],
            interpretations = kwargs['interpretations'],
            created_at = kwargs['created_at'],
            columns = kwargs['columns'],
            study_description = kwargs['study_description'],
            variables = kwargs['variables'],
            options = kwargs['options'],
            changes = kwargs['changes'],
            regression_configuration = kwargs['regression_configuration'],
            graphing = kwargs['graphing']
        )
    
    def delete_study(self):
        return self.db.delete_study(self.id)