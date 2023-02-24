from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utilities.time_util import utc_sec_to_date_time, spacetime_to_sun_based_time, spacetime_to_season
from flask_app.utilities.space_util import lat_to_natural_language, elev_m_to_elev_ft

class Living_thing:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']
        self.description = data['description']
        self.time_s = data['time_s']

        self.lat_deg = data['lat_deg']
        self.long_deg = data['long_deg']
        self.elev_m = data['elev_m']
        self.name_scientific = data['name_scientific']
        
        self.createdon_utc = data['createdon_utc']
        self.modifiedon_utc = data['modifiedon_utc']
    
    # in python OOP, there is something called a property, which defines
    # an attribute of the class object based on other attributes
    # the below property generates a correctly formatted url string for us
    # which we will be able to reference in our Jinja2 template
    @property
    def url_string(self):
        res_url_str = str(self.time_s)

        # split the name string into individual words
        # "john jacob jingle boy" -> ["john", "jacob", "jingle", "boy"]
        living_thing_name_array = self.name.split()

        # then we concatenate each item in the array onto the url_string
        for word in living_thing_name_array:
            res_url_str += "-"
            res_url_str += word

        return res_url_str

    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO living_things ( name, name_scientific, description, lat_deg, long_deg, elev_m, time_s ) \
        VALUES (%(name)s, %(name_scientific)s, %(description)s, %(lat_deg)s, %(long_deg)s, %(elev_m)s, %(time_s)s);"
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
    

    @classmethod
    def get_all( cls ):
        query_string = "SELECT * FROM living_things ORDER BY living_things.time_s DESC;"
        results = connectToMySQL().query_db(query_string)
        living_things = []
        for row in results:
            living_things.append( cls(row) )
        return living_things
    
    @classmethod
    def get_living_thing_by_id( cls, data ):
        query_string = "SELECT * FROM living_things WHERE id=%(id)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            living_thing = cls(results[0])
        else:
            living_thing = None
        return living_thing


    @classmethod
    def get_living_thing_by_time( cls, data ):
        query_string = "SELECT * FROM living_things WHERE time_s=%(time_s)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            living_thing = cls(results[0])
        else:
            living_thing = None
        return living_thing