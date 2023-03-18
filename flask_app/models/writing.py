from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utilities.time_util import utc_sec_to_date_time
from flask import Markup

class Writing:
    def __init__( self, data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.time_s = data['time_s']

        self.writing = Markup(data['writing'].replace('\n', '<br>'))

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
        writing_name_array = self.name.split()

        # then we concatenate each item in the array onto the url_string
        for word in writing_name_array:
            res_url_str += "-"
            res_url_str += word

        return res_url_str
    
    @property
    def time_string( self ):
        return utc_sec_to_date_time(self.time_s)

    @classmethod
    def get_all( cls ):
        query_string = "SELECT * FROM writings ORDER BY writings.time_s DESC;"
        results = connectToMySQL().query_db(query_string)
        writings = []
        for row in results:
            writings.append( cls(row) )
        return writings
    
    @classmethod
    def get_writing_by_id( cls, data ):
        query_string = "SELECT * FROM writings WHERE id=%(id)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            writing = cls(results[0])
        else:
            writing = None
        return writing

    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO writings ( name, writing, description, time_s ) \
            VALUES (%(name)s, %(writing)s, %(description)s, %(time_s)s);"
        return connectToMySQL().query_db(query_string, data)

    @classmethod
    def get_writing_by_time( cls, data ):
        query_string = "SELECT * FROM writings WHERE time_s=%(time_s)s;"
        results = connectToMySQL().query_db( query_string, data )
        if len(results) > 0:
            writing = cls(results[0])
        else:
            writing = None
        return writing