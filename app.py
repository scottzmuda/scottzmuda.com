from flask_app.controllers import (
    writingdex_controller,
    index_controller,
    writing_controller, 
    creature_controller,
    error_controller,
)
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)