from flask_app.config.mysqlconnection import connectToMySQL

class Creature:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.time_s = data['time_s']
        self.long_deg = data['long_deg']
        self.lat_deg = data['lat_deg']
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
        creature_name_array = self.name.split()

        # then we concatenate each item in the array onto the url_string
        for word in creature_name_array:
            res_url_str += "-"
            res_url_str += word

        return res_url_str

    @classmethod
    def get_all( cls ):
        query_string = "SELECT * FROM creatures ORDER BY creatures.time_s DESC;"
        results = connectToMySQL().query_db(query_string)
        creatures = []
        for row in results:
            creatures.append( cls(row) )
        return creatures
    
    @classmethod
    def get_creature_by_id( cls, data ):
        query_string = "SELECT * FROM creatures WHERE id=%(id)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            creature = cls(results[0])
        else:
            creature = None
        return creature

    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO creatures ( name, image, description ) \
            VALUES (%(name)s, %(image)s, %(description)s);"
        return connectToMySQL().query_db(query_string, data)

    @classmethod
    def get_creature_by_time( cls, data ):
        query_string = "SELECT * FROM creatures WHERE time_s=%(time_s)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            creature = cls(results[0])
        else:
            creature = None
        return creature