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