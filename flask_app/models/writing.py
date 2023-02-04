from flask_app.config.mysqlconnection import connectToMySQL

class writing:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']
        self.writing = data['writing']
        self.descriptino = data['description']

    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO writings ( name, image, writing, description ) \
            VALUES (%(name)s, %(image)s, %(writing)s, %(description)s);"
        return connectToMySQL().query_db(query_string, data)