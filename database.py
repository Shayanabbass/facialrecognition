import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceaccount.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facialattendence-15f63-default-rtdb.firebaseio.com/"
})
ref= db.reference('Students')
data={
    "B21110106074":{
        "name":"shayan",
        "seat no":"B21110106074",
        "Dept":"Computer Sci",
        "Major":"SE",
        "Semester":"5",
        "No_of_Attendence":"4",
        "last_attendence_time":"2024-04-30 00:54:34"

    }, "B21110106041":{
        "name":"Ahsan",
        "seat no":"B21110106041",
        "Dept":"Computer Sci",
        "Major":"SE",
        "Semester":"5",
        "No_of_Attendence":"4",

        "last_attendence_time":"2024-04-30 00:54:34"

    }, "B21110106040":{
        "name":"hadi",
        "seat no":"B21110106040",
        "Dept":"Computer Sci",
        "Major":"SE",
        "Semester":"5",
        "No_of_Attendence":"4",

        "last_attendence_time":"2024-04-30 00:54:34"

    },
    "B21110106016":{
        "name":"Azlan",
        "seat no":"B21110106016",
        "Dept":"Computer Sci",
        "Major":"SE",
        "Semester":"5",
        "No_of_Attendence":"4",

        "last_attendence_time":"2024-04-30 00:54:34"

    },
    "B21110106008":{
        "name":"Abdullah",
        "seat no":"B21110106008",
        "Dept":"Computer Sci",
        "Major":"SE",
        "Semester":"5",
        "No_of_Attendence":"4",

        "last_attendence_time":"2024-04-30 00:54:34"

    }

}
for key,value in data.items():
    ref.child(key).set(value)
