from flask_restful import Resource
from flask import request, after_this_request
import os, sys
import datetime
import hashlib
from loguru import logger
from email_validator import validate_email, EmailNotValidError
from .jwt import new_access_token, new_refresh_token
from database.functions import Select, Insert, Update

logger.add('logs/'+str(datetime.datetime.now().date())+'/users.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', filter="__main__", colorize=True, level='DEBUG')

def MD5Hash(password):
    result = hashlib.md5(password.encode())
    return result.hexdigest()


class Login(Resource):
    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/Login - '+str(request.remote_addr))
        try:
            request_body = request.json
            email = request_body["email"]
            password = request_body["password"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        password = MD5Hash(password)
        
        # return {"response": "success", "id": "public_id", "user_type": "user_type", "access_token": "access_token", "refresh_token": "refresh_token", "f_name": "fname", "l_name": "lname", "email": "email"}, 200
        
        login_response = Select("public_id, user_type, f_name, l_name, email, id", "users", " WHERE email='"+email+"' AND password='"+password+"'", 1)

        if(login_response == None):
            return {"response": "failed", "message": "Login failed!"}, 200
        elif(type(login_response) is tuple):
            public_id = login_response[0]
            user_type = login_response[1]
            if user_type == 1:
                user_type = "User"
            elif user_type == 0:
                user_type = "Admin"
            access_token = new_access_token(public_id)
            refresh_token = new_refresh_token(public_id)
            logger.info("Login successful - "+email)

            return {"response": "success", "id": public_id, "access_token": access_token, "refresh_token": refresh_token, "f_name": login_response[2], "l_name": login_response[3], "email": login_response[4]}, 200
        else:
            logger.info("Login failed - "+email+"\n"+str(login_response))
            return {"response": "failed", "message": "Login failed!", "description": str(login_response)}, 200
        
        
        
class Register(Resource):
    def post(self):
        logger.debug("------------------------------------------------")
        logger.info('/Register - '+str(request.remote_addr))
        try:
            request_body = request.json
            email = request_body["email"]
            password = request_body["password"]
            fname = request_body["fname"]
            lname = request_body["lname"]
            address = request_body["address"]
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("\nException: "+str(exception)+"\nLine: "+str(exc_tb.tb_lineno))
            return {"response": "error", "message": "Required fields are missing!"}, 403
        
        if(email == "" or password == "" or fname == "" or lname == "" or address == ""):
            logger.error("Registraion failed - empty values\n")
            return {"response": "error", "message": "One or more required fields are empty!"}, 403
        
        password = MD5Hash(password)
        public_id = MD5Hash(email+"+"+password+"@SwinTIP")
        insert_values = [(email, password, public_id, fname, lname, address)]
        register_response = Insert("users", "email, password, public_id, f_name, l_name, address", "%s, %s, %s, %s, %s, %s", insert_values)

        if register_response == 1:
            logger.info("Registration successful - "+email)
            return {"response": "success"}, 200
        else:
            logger.info("Registration failed - "+email+"\n"+str(register_response))
            if("Duplicate entry" in str(register_response) and "for key 'users.email'" in str(register_response)):
                register_response = "An account for the provided email already exists in the system."
            return {"response": "failed", "message": "Registration failed!", "description": str(register_response)}, 200

        