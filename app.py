from flask_app.controllers import (
    index_controller,
    creator_controller,
    writing_controller, 
    living_thing_controller,
    conversation_controller,
    error_controller,
)
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)