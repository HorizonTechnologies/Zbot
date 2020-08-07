#from db import conn
import db
import datetime

conn = db.db()

def show():
    try:
        cursor = conn.cursor()
        query = """select * from resources """
        cursor.execute(query)
        record = cursor.fetchall()
        #return record
        print(record)

        for res in record:
            print(res[0])
        return record
    except:
        print("err")
     
def insert(name, res, user):
    name = name.lower()
    res = res.lower()

    try:
        cursor = conn.cursor()
        query = """select * from resources where title = %s"""
        cursor.execute(query,(name, ))
        count = cursor.rowcount
        record = cursor.fetchall()
        
        #print(record)
        print(count)
        if count>=1:
            return "Duplicate title, Please choose a different title"
        #return record
        
        
        
    
        
        
        query = """ INSERT INTO resources ( slack_id,title, resource, ts) VALUES (%s,%s, %s, %s)"""
        
        insert = (user, name,res,datetime.datetime.now())
        
        cursor.execute(query, insert)

        conn.commit()
        count = cursor.rowcount
        
        return "successfully inserted "+ name+" - "+ res

    except:
        print("failed to insert")
               

def delete(_id):
    cursor = conn.cursor()
    _id = int(_id)
    
    
    query = """select * from resources where id = %s"""
    cursor.execute(query,(_id, ))
    count = cursor.rowcount
    if count<1:
        return "No record found, Refresh the resources"
    record = cursor.fetchone()
    
    query = """DELETE FROM resources WHERE id = %s"""
    cursor.execute(query,(_id,))
    count = cursor.rowcount
    conn.commit()
    return record[1]+" - "+record[2]+ "Successfully deleted"
    print(count)


  
