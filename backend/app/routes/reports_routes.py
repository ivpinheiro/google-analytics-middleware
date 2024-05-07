# Server imports
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request
from flask import send_from_directory

# Blueprints
flask_app_blueprint = Blueprint('main', __name__)

# Controllers imports
from app.controllers.GoogleAnalyticsController import GoogleAnalyticsController
from app.services.ProcessGoogleAnalyticsDataService import ProcessGoogleAnalyticsDataService

#Utils
import os

# Cors configuration
CORS(flask_app_blueprint)
@flask_app_blueprint.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST")
    return response

@flask_app_blueprint.route("/ga4/reports", methods=["POST"])
def process_post_data_ga4():
    if request.method == "POST":
        request_json = request.get_json()
    if request_json and "dataReports" in request_json:
        data = request_json["dataReports"]     
                       
        default_property_id = ""
        default_dimensions = []
        default_metrics = []
        default_start_date = ""
        default_end_date = ""
        
        property_id = data.get("property_id", default_property_id)
        dimensions = data.get("dimensions", default_dimensions)
        metrics = data.get("metrics", default_metrics)
        start_date = data.get("start_date", default_start_date)
        end_date = data.get("end_date", default_end_date)
        
        try:
            SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")
            response = GoogleAnalyticsController(SERVICE_ACCOUNT_FILE, property_id, dimensions, metrics, filter_field_name=None, filter_in_list_filter=None, key_is_path = False).get_google_analytics_data_ga4(start_date, end_date)            
            if not response:
                empty_data = {}
                return jsonify(empty_data), 200
            
            return jsonify(ProcessGoogleAnalyticsDataService(response).process_google_analytics_data_ga4()), 200
        except Exception as e:
            return jsonify({"error": "Ocorreu um erro ao inserir os dados"}), 500
        
@flask_app_blueprint.route("/ua/reports", methods=["POST"])
def process_post_data_ua():
    if request.method == "POST":
        request_json = request.get_json()
        if request_json and "dataReports" in request_json:
            data = request_json["dataReports"]     
            default_property_id = ""
            default_dimensions = []
            default_metrics = []
            default_start_date = ""
            default_end_date = ""
            
            property_id = data.get("property_id", default_property_id)
            dimensions = data.get("dimensions", default_dimensions)
            metrics = data.get("metrics", default_metrics)
            start_date = data.get("start_date", default_start_date)
            end_date = data.get("end_date", default_end_date)
            try:
                SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")
                response = GoogleAnalyticsController(SERVICE_ACCOUNT_FILE, property_id, dimensions, metrics, filter_field_name=None, filter_in_list_filter=None, key_is_path=False).get_google_analytics_data_ua(start_date, end_date)
                
                if not response:
                    empty_data = {}
                    return jsonify(empty_data), 200
                
                while response["reports"][0].get("nextPageToken"):
                    nextPageToken = response["reports"][0]["nextPageToken"]
                    response_ = GoogleAnalyticsController(SERVICE_ACCOUNT_FILE, property_id, dimensions, metrics, filter_field_name=None, filter_in_list_filter=None, key_is_path=False).get_google_analytics_data_ua(start_date, end_date, nextPageToken)
                    data = response["reports"][0]["data"]
                    rows = data.get("rows", [])
                    rows.extend(response_["reports"][0]["data"]["rows"])
                    response["reports"][0]["data"]["rows"] = rows
                    response["reports"][0]["nextPageToken"] = response_["reports"][0].get("nextPageToken")
                
                return jsonify(ProcessGoogleAnalyticsDataService(response).process_google_analytics_data_ua()), 200
            
            except Exception as e:
                return jsonify(f"{{'error': 'Ocorreu um erro ao inserir os dados', 'log_error': '{str(e)}'}}"), 500
            
@flask_app_blueprint.route("/api/documentation", methods=["GET"])
def process_get_data_swagger():
    swagger_json_path = os.path.join(os.getcwd(), 'app', 'static', 'swagger.json')
    if os.path.exists(swagger_json_path):
        return send_from_directory('app/static', 'swagger.json'), 200
    else:
        return jsonify({"error": "Swagger JSON not found"}), 404