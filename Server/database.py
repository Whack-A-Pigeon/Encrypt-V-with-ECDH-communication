# database.py
import pymysql
import hashlib

def connectToDatabase():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="AmanSingh197@", database="encryptiv_db")
        return connection
    except Exception as e:
        print(e)
        return None
