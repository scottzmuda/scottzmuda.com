from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utilities.time_util import utc_sec_to_date_time
from flask import Markup

class Taxon:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.name_definite = data['name_definite']
        self.description = data['description']
        self.taxon_id = data['taxon_id']
        self.taxon_plan_id = data['taxon_plan_id']

    # in python OOP, there is something called a property, which defines
    # an attribute of the class object based on other attributes

    @classmethod
    def get_taxon_by_id( cls, data ):
        query_string = "SELECT * FROM taxa WHERE id=%(id)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            taxon = cls(results[0])
        else:
            taxon = None
        return taxon

    #@classmethod
    #def get_taxonomy( self ):
    #    # Base case: if the taxon has no parent, return a list with only itself
    #    print(self.__dict__)
    #    if self.taxon_id is None:
    #        return [self]
    #    # Recursive case: get the parent taxon and prepend it to the list
    #    parent = self.get_taxon_by_id(self.taxon_id)
    #    return parent.get_taxonomy() + [self]
