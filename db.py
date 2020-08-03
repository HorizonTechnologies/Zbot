from datetime import datetime
import psycopg2
import json
def db():
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "123",
                                      host = "localhost",
                                      port = "3000",
                                      database = "postgres")

        
        
        return connection
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    
