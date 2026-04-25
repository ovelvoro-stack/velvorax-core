from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "status": "error",
            "message": e.description
        }), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500