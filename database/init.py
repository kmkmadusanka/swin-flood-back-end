import os
import mysql.connector
from mysql.connector import Error
from loguru import logger


def CreateDB():
  try:
    db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD")
    )
  except Error as exception:
    logger.error(exception)
    return "Database conncection error!"

  if db.is_connected():
    cursor = db.cursor()
    cursor.execute("DROP DATABASE "+os.getenv("DB_DATABASE"))
    cursor.execute("CREATE DATABASE "+os.getenv("DB_DATABASE"))
    return "Database created"
  else:
    return "Database not created"
  

def CreateTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()

  cursor.execute("""CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  f_name VARCHAR(20),
  l_name VARCHAR(20),
  email VARCHAR(50) UNIQUE,
  password VARCHAR(32),
  public_id VARCHAR(32) UNIQUE,
  user_type INT(1) DEFAULT 1 COMMENT '0-Admin, 1-User',
  address VARCHAR(225),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS safelocations (
  id INT NOT NULL AUTO_INCREMENT,
  address VARCHAR(225),
  geo_lat VARCHAR(5),
  geo_lng VARCHAR(5),
  distance VARCHAR(5),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS history (
  id INT NOT NULL AUTO_INCREMENT,
  date VARCHAR(10),
  geo_lat VARCHAR(5),
  geo_lng VARCHAR(5),
  rainfall VARCHAR(5),
  flood VARCHAR(5),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS discussions (
  id INT NOT NULL AUTO_INCREMENT,
  user_id VARCHAR(32),
  avatar VARCHAR(225) DEFAULT 'https://static.vecteezy.com/system/resources/previews/020/911/737/original/user-profile-icon-profile-avatar-user-icon-male-icon-face-icon-profile-icon-free-png.png',
  geo_lat VARCHAR(5),
  geo_lng VARCHAR(5),
  timestamp VARCHAR(20),
  message VARCHAR(225),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS severity (
  id INT NOT NULL AUTO_INCREMENT,
  geo_lat VARCHAR(5),
  geo_lng VARCHAR(5),
  address VARCHAR(225),
  severity VARCHAR(10),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS predictions (
  date VARCHAR(10),
  flood VARCHAR(5),
  severity VARCHAR(2),
  waterlevel VARCHAR(10),
  PRIMARY KEY (date))""")

  cursor.close()
  db.close()
  return "Tables created"


def DropTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()
  cursor.execute("DROP TABLE users;")
  cursor.execute("DROP TABLE safelocations;")
  cursor.execute("DROP TABLE history;")
  cursor.execute("DROP TABLE discussions;")
  cursor.execute("DROP TABLE severity;")
  cursor.execute("DROP TABLE predictions;")
  db.commit()
  cursor.close()
  db.close()
  return "Tables dropped"


def TruncateTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()
  # cursor.execute("TRUNCATE TABLE users;")
  # cursor.execute("TRUNCATE TABLE safelocations;")
  # cursor.execute("TRUNCATE TABLE history;")
  # cursor.execute("TRUNCATE TABLE discussions;")
  # cursor.execute("TRUNCATE TABLE severity;")
  cursor.execute("TRUNCATE TABLE predictions;")
  db.commit()
  cursor.close()
  db.close()
  return "Tables truncated"


def DummyData():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      port = os.getenv("DB_PORT"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()

  cursor.execute("""INSERT IGNORE INTO users (f_name, l_name, email, password, public_id, user_type) VALUES 
  ('Dinuka', 'dinuka@swintip.com', '1146b6c258a28b28941c57851ee084a1', '94da13d942686d452842ac61adf3bad4', 1, 1),
  ('Kasun', 'kasun@swintip.com', '1146b6c258a28b28941c57851ee084a1', 'b453d1a0900d948bfa4df3437dc27eae', 1, 1),
  ('Nuwanga', 'nuwanga@swintip.com', '1146b6c258a28b28941c57851ee084a1', 'a65c350db098e3a187a8210295216354', 1, 1),
  ('Sachie', 'sachie@swintip.com', '1146b6c258a28b28941c57851ee084a1', '2f62964015b3db835a5d4dda15ef8245', 1, 1),
  ('Lahiru', 'lahiru@swintip.com', '1146b6c258a28b28941c57851ee084a1', '182ea55668cb81b2f0dd98bfbe3b26ea', 1, 1),
  ('Admin', 'admin1@swintip.com', '1146b6c258a28b28941c57851ee084a1', 'ce29c11c6abede16028b9fd12642ffc7', 1, 1),
  ('User', 'user1@swintip.com', '1146b6c258a28b28941c57851ee084a1', '385dfe8949163253ec44a73bf876ea56', 0, 1);
  """)

  db.commit()
  cursor.close()
  db.close()
  return "Dummy data inserted"
