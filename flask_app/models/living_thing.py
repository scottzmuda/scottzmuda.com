from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, Markup
from flask_app.utilities.time_util import utc_sec_to_date_time, spacetime_to_sun_based_time, spacetime_to_season
from flask_app.utilities.space_util import lat_to_natural_language, elev_m_to_elev_ft, natural_elevation
from flask_app.utilities.num_util import test_valid_floating_point
import re
from datetime import datetime

name_regex = re.compile(r'^[a-zA-Z\-\s]+$')
name_scientific_regex = re.compile(r'^[a-zA-Z\-\s]+$')
description_regex = re.compile(r'^[a-zA-Z\-\.\?\"\'!,\s]+$')

class Living_thing:
    def __init__( self, data ):       
        #identity
        self.id = data['id']
        self.image = data['image']

        #coordinates
        self.time_s = data['time_s']
        self.lat_deg = data['lat_deg']
        self.long_deg = data['long_deg']
        self.elev_m = data['elev_m']

        #groups
        self.formal_name = data['formal_name']
        self.common_name = data['common_name']
        self.taxonomy = None

        #note
        self.note = Markup(data['note'].replace('\n', '<br>'))

        #admin
        self.status = data['status']
        self.creator = data['creator']

    # in python OOP, there is something called a property, which defines
    # an attribute of the class object based on other attributes
    # the below property generates a correctly formatted url string for us
    # which we will be able to reference in our Jinja2 template
    @property
    def url_string(self):
        res_url_str = str(self.time_s)

        # split the name string into individual words
        # "john jacob jingle boy" -> ["john", "jacob", "jingle", "boy"]
        living_thing_name_array = self.common_name.split()

        # then we concatenate each item in the array onto the url_string
        for word in living_thing_name_array:
            res_url_str += "-"
            res_url_str += word

        return res_url_str

#used for individual living thing page
    @classmethod
    def get_living_thing_by_time( cls, data ):
        query_string = """
        SELECT o.id, o.image, o.time_s, o.lat_deg, o.long_deg, o.elev_m, o.status, c.name_id AS creator, fk.name AS formal_name, ck.name AS common_name, o.note
        
        FROM observations o
        JOIN creators c ON o.creator_id = c.id
        JOIN observation_common_kinds ock ON ock.observation_id = o.id
        JOIN common_kinds ck ON ock.common_kind_id = ck.id
        JOIN observation_formal_kinds ofk ON ofk.observation_id = o.id
        JOIN formal_kinds fk ON ofk.formal_kind_id = fk.id
        
        WHERE o.time_s=%(time_s)s
        """
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            living_thing = cls(results[0])
        else:
            living_thing = None
        return living_thing

#used for living thing feed
    @classmethod
    def get_all( cls ):
        query_string = """
        SELECT o.id, o.image, o.time_s, o.lat_deg, o.long_deg, o.elev_m, o.status, c.name_id AS creator, fk.name AS formal_name, ck.name AS common_name, o.note
        
        FROM observations o
        JOIN creators c ON o.creator_id = c.id
        JOIN observation_common_kinds ock ON ock.observation_id = o.id
        JOIN common_kinds ck ON ock.common_kind_id = ck.id
        JOIN observation_formal_kinds ofk ON ofk.observation_id = o.id
        JOIN formal_kinds fk ON ofk.formal_kind_id = fk.id
        WHERE o.status != 1 OR o.status IS NULL
        ORDER BY o.time_s DESC;
        """
        results = connectToMySQL().query_db(query_string)
        print(type(results))
        living_things = []
        for row in results:
            living_things.append( cls(row) )
        return living_things

#used to generate taxonomy list
    def generate_taxonomy(self):
        query_string = """
            WITH RECURSIVE TaxaHierarchy AS (
                SELECT t.parent_id, ck.name AS 'child'
                FROM taxonomy t
                JOIN formal_kinds fk ON t.child_id = fk.id
                JOIN common_kinds ck ON ck.formal_kind_id = fk.id
                JOIN observation_formal_kinds ofk ON ofk.formal_kind_id = fk.id
                JOIN observations o ON ofk.observation_id = o.id
                WHERE o.id = %(observation_id)s
                
                UNION ALL
                
                SELECT t.parent_id, ck.name AS 'child'
                FROM taxonomy t
                JOIN TaxaHierarchy th ON th.parent_id = t.child_id
                JOIN formal_kinds fk ON t.child_id = fk.id
                JOIN common_kinds ck ON ck.formal_kind_id = fk.id
            )
            SELECT child
            FROM TaxaHierarchy;
        """

        data = {
            "observation_id": self.id
        }

        # Assuming connectToMySQL() is a function that connects to the database
        results = connectToMySQL().query_db(query_string, data)

        # Assign the results directly to self.taxonomy
        taxonomy = [row["child"] for row in results]

        self.taxonomy = taxonomy

    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO living_things ( creator_id, lat_deg, long_deg, elev_m, time_s ) \
        VALUES (%(creator_id)s, %(lat_deg)s, %(long_deg)s, %(elev_m)s, %(time_s)s);"
        return connectToMySQL().query_db(query_string, data)
    





    @property
    def time_string( self ):
        return utc_sec_to_date_time(self.time_s)

    @property
    def sun_based_time( self ):
        return spacetime_to_sun_based_time(self.time_s, self.lat_deg, self.long_deg, self.elev_m)

    @property 
    def season( self ):
        return spacetime_to_season(self.time_s, self.lat_deg, self.long_deg, self.elev_m)

    @property
    def natural_language_latitude( self ):
        return lat_to_natural_language(self.lat_deg)

    @property
    def elev_ft( self ):
        return elev_m_to_elev_ft(self.elev_m)

    @property
    def natural_elevation( self ):
        return natural_elevation(self.elev_m)

    
    @staticmethod
    def validate_living_thing_form(data):
        # this is slightly hacky
        # most languages support a concept called 'pass by reference'
        # which means that when a variable is passed to a function
        # what is really happening is that a 'pointer' variable is being passed
        # so if the value of that variable is modified by the function,
        # then the original variable is also modified
        # python language handles variables differently, so I'm using the following dictionary
        # to 'hack' my way around this. Thus making the code simpler to follow.
        is_valid = {'pass_by_reference': True}

        #Living_thing.validate_name(data['name'], is_valid)
        #Living_thing.validate_name_scientific(data['name_scientific'], is_valid)
        Living_thing.validate_description(data['description'], is_valid)
        Living_thing.validate_long_deg(data['long_deg'], is_valid)
        Living_thing.validate_lat_deg(data['lat_deg'], is_valid)
        Living_thing.validate_elev_m(data['elev_m'], is_valid)
        Living_thing.validate_date_time(data['date_time'], is_valid)

        return is_valid['pass_by_reference']
    
    #@staticmethod
    #def validate_name(form_name, is_valid):
    #    if not name_regex.match(form_name):
    #        flash("name must contain only characters a-z, A-Z, -", "create_living_thing")
    #        is_valid['pass_by_reference'] = False
    
    #@staticmethod
    #def validate_name_scientific(form_name_scientific, is_valid):
    #    if not name_scientific_regex.match(form_name_scientific):
    #        flash("scientific name must contain only characters a-z, A-Z, -", "create_living_thing")
    #        is_valid['pass_by_reference'] = False

    #@staticmethod
    #def validate_description(form_description, is_valid):
    #    if not description_regex.match(form_description):
    #        flash("description must contain only characters a-z, A-Z, 0-9, - , \' \" . ? !", "create_living_thing")
    #        is_valid['pass_by_reference'] = False

    @staticmethod
    def validate_long_deg(form_long_deg, is_valid):
        if not test_valid_floating_point(form_long_deg):
            flash("longitude must be a number", "create_living_thing")
            is_valid['pass_by_reference'] = False
            return
        
        long_deg_float = float(form_long_deg)

        if long_deg_float > 180:
            flash("longitude cannot be greater than 180 degrees", "create_living_thing")
            is_valid['pass_by_reference'] = False
        elif long_deg_float < -180:
            flash("longitude cannot be less than -180 degrees", "create_living_thing")
            is_valid['pass_by_reference'] = False

    @staticmethod
    def validate_lat_deg(form_lat_deg, is_valid):
        if not test_valid_floating_point(form_lat_deg):
            flash("latitude must be a number", "create_living_thing")
            is_valid['pass_by_reference'] = False
            return
        
        lat_deg_float = float(form_lat_deg)

        if lat_deg_float > 90:
            flash("latitude cannot be greater than 90 degrees", "create_living_thing")
            is_valid['pass_by_reference'] = False
        elif lat_deg_float < -90:
            flash("latitude cannot be less than -90 degrees", "create_living_thing")
            is_valid['pass_by_reference'] = False

    @staticmethod
    def validate_elev_m(form_elev_m, is_valid):
        if not test_valid_floating_point(form_elev_m):
            flash("elevation must be a number", "create_living_thing")
            is_valid['pass_by_reference'] = False
            return
        
        elev_m_float = float(form_elev_m)

        if elev_m_float > 15000:
            flash("elevation cannot be greater than 15,000 meters", "create_living_thing")
            is_valid['pass_by_reference'] = False
        elif elev_m_float < -15000:
            flash("elevation cannot be less than -15,000 meters", "create_living_thing")
            is_valid['pass_by_reference'] = False

    @staticmethod
    def validate_date_time(form_date_time, is_valid):
        try:
            datetime.strptime(form_date_time, '%Y-%m-%dT%H:%M')
        except:
            flash("date must be a valid date-time format", "create_living_thing")
            is_valid['pass_by_reference'] = False