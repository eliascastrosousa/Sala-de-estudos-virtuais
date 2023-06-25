import pyrebase

config = {
    "apiKey": "AIzaSyCe4NkZfSUDNh7S4W0f9XDf_s3QysSv1ec",
    "authDomain": "sala-de-estudos-virtuais.firebaseapp.com",
    "databaseURL": "https://sala-de-estudos-virtuais-default-rtdb.firebaseio.com",
    "projectId": "sala-de-estudos-virtuais",
    "storageBucket": "sala-de-estudos-virtuais.appspot.com",
    "messagingSenderId": "866598182752",
    "appId": "1:866598182752:web:aab9e844002ab79d548805",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
