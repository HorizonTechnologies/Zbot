from db import conn

db = conn()
def resources():
    
    check = db.child("resources").get()
    resource =[]
    if check.val()!=None:
        for l in check:
            s = l.val()
            for k in s.keys():
                out =  k
                out = out +" - "+s[k]
                resource.append(out)
        print("resources displayed")
        return resource
    
                
                
def insert(name, res):
    name = name.lower()
    res = res.lower()
    check = db.child("resources").get()
    insert = True
    if check.val()==None:
        db.child("resources").push({name : res})
    else:
        for l in check:
            s = l.val()
            for k in s.keys():
                if k == name:
                    return "Duplicate name"
        print("resource inserted")    
        db.child("resources").push({name : res})

def delete(name):
    check = db.child("resources").get()
    if check.val()!=None:
        for l in check:
            s = l.val()
            for k in s.keys():
                if k == name:
                    rem = l.key()
                    db.child("resources").child(rem).remove()
                    return "Deleted successfully"

