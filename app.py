import os
import datetime
from datetime import timedelta
from dotenv import load_dotenv
from loguru import logger
from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from src.routes import initialize_routes

logger.add('logs/'+str(datetime.datetime.now().date())+'/app.log', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', filter="__main__", colorize=True, level='DEBUG')


# load .env variables
load_dotenv()


# init server
app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/": {"origins": "*"}})
api = Api(app)


# init api routes
initialize_routes(api)


# JWT Token configs
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)


# server health check endpoint
@app.route("/", methods=["GET", "POST"])
def health():
    return "Backend server is running"


# run Server
if __name__ == "__main__":
    app.run(
        host = os.getenv("HOST_NAME"), 
        port = os.getenv("PORT"), 
        debug = os.getenv("APP_DEBUG")
        )