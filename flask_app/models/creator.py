from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#define global reg expressions for data validation
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_id_regex = re.compile(r'^[a-zA-Z0-9]+$')
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$')

class Creator:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.name_id = data['name_id']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.createdon_utc = data['createdon_utc']
        self.modifiedon_utc = data['modifiedon_utc']
        self.writings = {}
        self.living_things = {}
    
    #CREATE
    @classmethod
    def save( cls, data ):
        query_string = "INSERT INTO creators ( name, name_id, email, password_hash ) VALUES \
            ( %(name)s, %(name_id)s, %(email)s, %(password_hash)s );"
        user_id = connectToMySQL().query_db( query_string, data )
        return user_id

    #READ
    @classmethod
    def get_creator_by_email( cls, data ):
        query_string = "SELECT * FROM creators WHERE creators.email=%(email)s;"
        results = connectToMySQL().query_db(query_string, data)
        if len(results) > 0:
            creator = cls(results[0])
        else:
            creator = None
        return creator
    
    @classmethod
    def get_creator_by_name_id( cls, data ):
        query_string = "SELECT * FROM creators WHERE creators.name_id=%(name_id)s;"
        results = connectToMySQL().query_db(query_string, data)
        if len(results) > 0:
            creator = cls(results[0])
        else:
            creator = None
        return creator

    @staticmethod
    def validate_registration_form(data):
        is_valid = True
        # name validations
        # must be at least 1 characters
        if len(data['name']) < 1:
            flash("name must be at least 1 character long", "register")
            is_valid = False
        # must be less than 50 characters
        elif len(data['name']) > 50:
            flash("name must be 50 characters or less", "register")
            is_valid = False
        # name_id validations
        # must be at least 4 character
        if len(data['name_id']) < 4:
            flash("name_id must be at least 4 characters long", "register")
            is_valid = False
        # must be 15 characters or less
        elif len(data['name_id']) > 15:
            flash("name_id must be 15 characters or less", "register")
            is_valid = False
        # must match regex, requiring only alpha-numeric characters
        elif not name_id_regex.match(data['name_id']):
            flash("name_id must be alpha-numeric", "register")
            is_valid = False
        # confirm name_id is not already used for another account
        elif Creator.get_creator_by_name_id(data):
            flash("account already exists for this login_id", "register")
            is_valid = False
        # email validations
        # must match valid email structure
        if not email_regex.match(data['email']):
            flash("must enter a valid email address", "register")
            is_valid = False
        # confirm email is not already used for another account
        elif Creator.get_creator_by_email(data):
            flash("account already exists for this email", "register")
            is_valid = False
        # password validations
        # must be 8 characters
        if len(data['password']) < 8:
            flash("password must be at least 8 characters", "register")
            is_valid = False
        # must match regex, requiring one of each: uppercase, lowercase, number
        elif not password_regex.match(data['password']):
            flash("password must contain at least 1 uppercase, 1 lowercase, 1 number", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def hash_password(data):
        password_hash = bcrypt.generate_password_hash(data['password'])
        return password_hash
    
    @staticmethod
    def validate_login_form(data):
        if not email_regex.match(data['email']):
            flash("must enter a valid email address", "login")
            return False
        return True
    
    @staticmethod
    def verify_login_credentials( data ):
        creator = Creator.get_creator_by_email(data)
        if not creator:
            flash("no account for that email was not found", "login")
            return False
        if len(data['password']) < 8:
            flash("sorry, incorrect password", "login")
            return False
        if not bcrypt.check_password_hash(creator.password_hash, data['password']):
            flash("sorry, incorrect password", "login")
            return False
        return creator.id
