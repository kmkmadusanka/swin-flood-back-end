from flask_restful import Resource
from flask import request, after_this_request
import os, sys
import datetime
from loguru import logger
from .jwt import new_access_token, new_refresh_token
from database.functions import Select, Insert, Update

logger.add('logs/'+str(datetime.datetime.now().date())+'/discussion.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', filter="__main__", colorize=True, level='DEBUG')

class Discussion(Resource):
    def get(self):
        logger.debug("------------------------------------------------")
        logger.info('/Discussion (Get) - '+str(request.remote_addr))

        db_response = Select("id, user_id, geo_lat, geo_lng, avatar, timestamp, message", "discussions", "", 0)

        if(db_response == None):
            return {"response": "failed", "message": "Discussions not found!"}, 200
        elif(type(db_response) is list):
            response = {}
            response["response"] = "success"
            discussions = []
            for discussion in db_response:
                discussions.append({"id":str(discussion[0]), "user":str(discussion[1]), "geo":[float(discussion[2]), float(discussion[3])], "avatar":str(discussion[4]), "timestamp":str(discussion[5]), "message":str(discussion[6])})
            response["discussions"] = discussions
            return response
        else:
            logger.info("Discussions not found \n"+str(db_response))
            return {"response": "failed", "message": "Discussions not found!", "description": str(db_response)}, 200
        
        
    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/Discussion (Post) - '+str(request.remote_addr))
        try:
            request_body = request.json
            user = request_body["user"]
            message = request_body["message"]
            geo = request_body["location"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403

        if(user == "" or message == ""):
            logger.error("Discussion post failed - empty values\n")
            return {"response": "error", "message": "One or more required fields are empty!"}, 403
        
        insert_values = [(user, str(geo[0]), str(geo[1]), str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")), message)]
        insert_response = Insert("discussions", "user_id, geo_lat, geo_lng, timestamp, message", "%s, %s, %s, %s, %s", insert_values)

        if insert_response == 1:
            logger.info("Discussion posted")
            return {"response": "success"}, 200
        else:
            logger.info("Discussion post failed \n"+str(insert_response))
            return {"response": "failed", "message": "Discussion post failed!", "description": str(insert_response)}, 200

        