import os
import mysql.connector
from mysql.connector import Error
from loguru import logger

def Select(select_fields, select_table, select_conditions, count):
  try:
    db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
    cursor = db.cursor()
    cursor.execute("SELECT "+select_fields+" FROM "+select_table+select_conditions)
    if count == 1:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
  except Error as exception:
    logger.error("Database Exception: "+str(exception))
    return str(exception.msg)
    

def Insert(insert_table, insert_fields, insert_value_placeholder, insert_values):
  try:
    db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
    cursor = db.cursor()
    cursor.executemany("INSERT INTO "+insert_table+" ("+insert_fields+") VALUES ("+insert_value_placeholder+")", insert_values)
    db.commit()
    return cursor.rowcount
  except Error as exception:
    logger.error("Database Exception: "+str(exception))
    return str(exception.msg)
    

def Update(update_table, update_fields, update_where):
  try:
    db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
    cursor = db.cursor()
    cursor.execute("UPDATE "+update_table+" SET "+update_fields+" WHERE "+update_where+";")
    db.commit()
    return cursor.rowcount
  except Error as exception:
    logger.error("Database Exception: "+str(exception))
    return str(exception.msg)