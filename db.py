
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def db():
    """
    postgres DB Connections
    getting user, password,host,port, database variables from environment

    """
    try:
        
        user =  os.getenv("user")
        password = os.getenv("password")
        host = os.getenv("host")
        port = os.getenv("port")
        database = os.getenv("database")
        
        connection = psycopg2.connect(user =user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)

        
        
        return connection
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    
