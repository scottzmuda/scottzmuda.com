from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utilities.time_util import utc_sec_to_date_time
from flask import Markup

class Species:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.name_definite = data['name_definite']
        self.description = data['description']
        self.biblical_taxon_id = data['biblical_taxon_id']

    # in python OOP, there is something called a property, which defines
    # an attribute of the class object based on other attributes

    @classmethod
    def get_species_by_id( cls, data ):
        query_string = "SELECT * FROM species WHERE id=%(id)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            species = cls(results[0])
        else:
            species = None
        return species