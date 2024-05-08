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
        
        # return {"response": "success", "locations": [{"geo": [0.0, 0.0], "address": "address", "distance":"0km"},{"geo": [0.0, 0.0], "address": "address", "distance":"0km"}]}, 200

    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/SafeLocations (Post) - '+str(request.remote_addr))
        # return {"response": "success", "message": "Safe location recorded successfully!"}, 200
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
        logger.info('/SafeLocations - '+str(request.remote_addr))
        
        return {"response": "success", "locations": [{"date": "2021/01/01", "rainfall": "30", "flood":"10"},{"date": "2021/01/01", "rainfall": "30", "flood":"10"}]}, 200

