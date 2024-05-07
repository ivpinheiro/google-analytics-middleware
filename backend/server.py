# Server imports
from flask import Flask
from app.routes import reports_routes
from flask_swagger_ui import get_swaggerui_blueprint

# Dev environment
# from dotenv import load_dotenv
# load_dotenv()

#Utils
import os

# Init flask app
app = Flask(__name__)

SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI (without trailing "/")
API_URL =  "/api/documentation"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

# Register app in Blueprint
app.register_blueprint(reports_routes)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)