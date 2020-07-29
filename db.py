import pyrebase

def conn():
    config = {
        "apiKey": "AIzaSyAPKL-MQVLicodVmUuOWCnR-SgyKs2U_xs",
        "authDomain": "test-31c49.firebaseapp.com",
        "databaseURL": "https://test-31c49.firebaseio.com",
        "projectId": "test-31c49",
        "storageBucket": "test-31c49.appspot.com",
        "messagingSenderId": "284466329659",
     
        }
    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    return db
