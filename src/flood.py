from flask_restful import Resource
from flask import request, after_this_request
import os, sys
import datetime
from loguru import logger
from database.functions import Select, Insert, Update

logger.add('logs/'+str(datetime.datetime.now().date())+'/flood.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', filter="__main__", colorize=True, level='DEBUG')

class SafeLocations(Resource):
    def get(self):
        logger.debug("------------------------------------------------")
        logger.info('/SafeLocations (Get) - '+str(request.remote_addr))

        db_response = Select("id, address, geo_lat, geo_lng, distance", "safelocations", "", 0)

        if(db_response == None):
            return {"response": "failed", "message": "Safe locations not found!"}, 200
        elif(type(db_response) is list):
            response = {}
            response["response"] = "success"
            locations = []
            for location in db_response:
                locations.append({"id":str(location[0]), "address":str(location[1]), "geo":[float(location[2]), float(location[3])], "distance":str(location[4])})
            response["locations"] = locations
            return response
        else:
            logger.info("Safe locations failed \n"+str(db_response))
            return {"response": "failed", "message": "Safe locations not found!", "description": str(db_response)}, 200
        

    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/SafeLocations (Post) - '+str(request.remote_addr))
        try:
            request_body = request.json
            geo = request_body["geo"]
            address = request_body["address"]
            distance = request_body["distance"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        if(geo == "" or address == "" or distance == ""):
            logger.error("Registraion failed - empty values\n")
            return {"response": "error", "message": "One or more required fields are empty!"}, 403

        insert_values = [(address, str(geo[0]), str(geo[1]), distance)]
        register_response = Insert("safelocations", "address, geo_lat, geo_lng, distance", "%s, %s, %s, %s", insert_values)

        if register_response == 1:
            logger.info("Safe location recorded successfully")
            return {"response": "success"}, 200
        else:
            logger.info("Safe location recording failed \n"+str(register_response))
            return {"response": "failed", "message": "Safe location recording failed!", "description": str(register_response)}, 200


class FloodHistory(Resource):
    def get(self):
        logger.debug("------------------------------------------------")
        logger.info('/FloodHistory (Get) - '+str(request.remote_addr))

        db_response = Select("id, date, geo_lat, geo_lng, rainfall, flood", "history", "", 0)

        if(db_response == None):
            return {"response": "failed", "message": "Flood history not found!"}, 200
        elif(type(db_response) is list):
            response = {}
            response["response"] = "success"
            locations = []
            for location in db_response:
                locations.append({"id":str(location[0]), "date":str(location[1]), "geo":[float(location[2]), float(location[3])], "rainfall":str(location[4]), "flood":str(location[5])})
            response["history"] = locations
            return response
        else:
            logger.info("Flood history failed \n"+str(db_response))
            return {"response": "failed", "message": "Flood history not found!", "description": str(db_response)}, 200
        

    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/FloodHistory (Post) - '+str(request.remote_addr))
        try:
            request_body = request.json
            date = request_body["date"]
            rainfall = request_body["rainfall"]
            flood = request_body["flood"]
            geo = request_body["geo"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        if(geo == "" or date == "" or rainfall == "" or flood == ""):
            logger.error("Registraion failed - empty values\n")
            return {"response": "error", "message": "One or more required fields are empty!"}, 403

        insert_values = [(date, str(geo[0]), str(geo[1]), flood, rainfall)]
        register_response = Insert("history", "date, geo_lat, geo_lng, flood, rainfall", "%s, %s, %s, %s, %s", insert_values)

        if register_response == 1:
            logger.info("Flood history recorded successfully")
            return {"response": "success"}, 200
        else:
            logger.info("Flood history recording failed \n"+str(register_response))
            return {"response": "failed", "message": "Flood history recording failed!", "description": str(register_response)}, 200


class FloodSeverity(Resource):
    def get(self):
        logger.debug("------------------------------------------------")
        logger.info('/FloodSeverity (Get) - '+str(request.remote_addr))

        db_response = Select("id, address, geo_lat, geo_lng, severity", "severity", "", 0)

        if(db_response == None):
            return {"response": "failed", "message": "Flood severity not found!"}, 200
        elif(type(db_response) is list):
            response = {}
            response["response"] = "success"
            locations = []
            for location in db_response:
                locations.append({"id":str(location[0]), "address":str(location[1]), "geo":[float(location[2]), float(location[3])], "severity":str(location[4])})
            response["severity"] = locations
            return response
        else:
            logger.info("Flood severity failed \n"+str(db_response))
            return {"response": "failed", "message": "Flood severity not found!", "description": str(db_response)}, 200
        

    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/FloodSeverity (Post) - '+str(request.remote_addr))
        try:
            request_body = request.json
            address = request_body["address"]
            severity = request_body["severity"]
            geo = request_body["geo"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        if(geo == "" or address == "" or severity == ""):
            logger.error("Registraion failed - empty values\n")
            return {"response": "error", "message": "One or more required fields are empty!"}, 403

        insert_values = [(address, str(geo[0]), str(geo[1]), severity)]
        register_response = Insert("severity", "address, geo_lat, geo_lng, severity", "%s, %s, %s, %s", insert_values)

        if register_response == 1:
            logger.info("Flood severity recorded successfully")
            return {"response": "success"}, 200
        else:
            logger.info("Flood severity recording failed \n"+str(register_response))
            return {"response": "failed", "message": "Flood severity recording failed!", "description": str(register_response)}, 200

