from flask_restful import Resource
from flask import request, after_this_request
import os, sys
import datetime
import json
import requests
from loguru import logger
from database.functions import Select, Insert
from database.init import TruncateTables
from src.email import sendEmail

logger.add('logs/'+str(datetime.datetime.now().date())+'/prediction.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', filter="__main__", colorize=True, level='DEBUG')

class Predict(Resource):
    def get(self):
        logger.debug("------------------------------------------------")
        logger.info('/Predict (get) - '+str(request.remote_addr))
        
        start_date = datetime.datetime.now().strftime("%Y/%m/%d")
        end_date =  (datetime.datetime.now()+datetime.timedelta(days=30)).strftime("%Y/%m/%d")
        db_response = Select("date, flood, severity, waterlevel", "predictions", " WHERE (date BETWEEN '"+start_date+"' AND '"+end_date+"')", 0)

        if(db_response == None):
            return {"response": "failed", "message": "predictions not found!"}, 200
        elif(type(db_response) is list):
            response = {}
            response["response"] = "success"
            predictions = []
            for prediction in db_response:
                predictions.append({"date":str(prediction[0]), "flood":str(prediction[1]), "severity":str(prediction[2]), "waterlevel":str(prediction[3])})
            response["predictions"] = predictions
            return response
        else:
            logger.info("predictions retrieve failed")
            return {"response": "failed", "message": "predictions retrieve failed!", "description": str(db_response)}, 200

    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/Predict (post) - '+str(request.remote_addr))
        try:
            request_body = request.json
            data = request_body["data"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        url = "http://52.206.147.8/predict"
        headers = {
            'Content-Type': 'application/json'
            }
        
        email_alert = ""
        insert_values = []
        for payload in data:
            prediction_date = payload["date"]
            payload = json.dumps(payload)
            response = requests.request("POST", url, headers=headers, data=payload)
            prediction = json.loads(response.text)
            insert_values.append((prediction_date, prediction["floodRisk"], prediction["severity"], "%.2f" % prediction["waterLevel"]))
            if(str(prediction["floodRisk"]) == "true"):
                email_alert = email_alert+"+ "+str(prediction_date)+" - Flood risk with a severity of "+str(prediction["severity"])+"<br>"
                
        if(email_alert != ""):
            sendEmail(email_alert)
            
        if(TruncateTables() == "Tables truncated"):
            db_response = Insert("predictions", "date, flood, severity, waterlevel", "%s, %s, %s, %s", insert_values)

            if db_response != 0:
                logger.info("Mock data saved successfully - "+str(db_response)+" records saved.")
                return {"response": "success", "message": str(db_response)+" records saved."}, 200
            else:
                logger.info("Mock data saving failed \n"+str(db_response))
                return {"response": "failed", "message": "Mock data saving failed!", "description": str(db_response)}, 200
        else:
            return {"response": "failed", "message": "Table truncate failed!",}, 200

