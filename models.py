"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *
from pydal.validators import IS_NOT_EMPTY, IS_IN_SET


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

# For table 'user':
# username = the user's username
# password = the user's password
# firstName = the user's first name
# lastName = the user's last name
# category = if the user is a rider or driver
# carMake, carModel = the user's car's make and model
# numSeats = the user's car's number of seats
# location = the user's nearest ideal pickup location
# schedule = a list of the user's on-campus schedule

db.define_table('user',
                Field('user_id', 'reference auth_user'),
                Field('username'),
                Field('password'),
                Field('profilePic', 'text'),
                Field('firstName'),
                Field('lastName'),
                Field('category', requires=IS_IN_SET(['Driver','Rider'])),
                Field('carMake'),
                Field('carModel'),
                Field('numSeats'),
                Field('location'),
                Field('schedule', 'string'),
                Field('license', 'string'),
                Field('monday', 'string'),
                Field('tuesday', 'string'),
                Field('wednesday', 'string'),
                Field('thursday', 'string'),
                Field('friday', 'string'),
                Field('saturday', 'string'),
                Field('sunday', 'string'),
                )

db.define_table(
    'user_schedule',
    Field('user_id', 'reference: user'),
    Field('day_of_week'),
    Field('available_time')
    )

#just added messages table
db.define_table('user_message',
    Field('user_id', 'reference auth_user'),
    # Field('username', 'string'), #new
    Field('text', 'text'),

    # store the user id of the user you are messaging
    Field('otherUserID'),

    # store timestamp for sorting display 
    Field('timestamp')
)

#just added messages table
db.define_table('tempID',
    Field('id'),
)

# db.executesql('DELETE FROM user_message;')

db.commit()

locationList = [("Porter", 36, 122), ("College 9", 37.0015833, -122.0572618), ("Kresge", 36.9979, -122.06595), ("College 10", 37.000860, -122.058100), ("Stevenson", 36.997695, -122.052059),
("Merril", 37.00030, -122.05291), ("Crown", 37.000461, -122.054731), ("Cowell", 36.996950, -122.053894), ("Nobel", 36.975479, -122.054101), ("Escalona", 36.970805, -122.044747), ("Downtown", 36.972641, -122.025816), ("Natural Bridges", 36.9524511, -122.0574637), 
("WatsonVille", 36.910233, -121.756897), ("Seabright", 36.9632839, -122.0080175), ("Capitola", 36.98, -121.95), ("Ocean st", 36.97176, -122.01761), ("Soquel", 36.988327, -121.956696), ("Scotts Valley", 37.0508, -122.0080)]

model = ["Ford F150", "Ford F350", "Honda Civic", "Honda Accord", "Honda CRV",
"Toyota Supra", "Toyota Corolla", "Toyota Camry", "Toyota Prius", "Subaru WRX", 
"Lambrogini", "Rolls Royce Phantom", "Volkswagen Golf", "Ford Fusion", "Ford Fiesta", 
"Volkswagen Beetle", "Audi A3", "Chevrolet Impala", "GMC Sierra", "Dodge Ram", 
"Dodge Charger", "Toyota Tacoma" ]

days_of_week = ["Monday", "Tuesday","Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

r_times = ["9:00 am" , "10:00 am", "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm","3:00 pm", "4:00 pm"]

nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

lets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def add_users_for_testing(num_users):
     # Test user names begin with "_".
    # Counts how many users we need to add.
    db(db.user.username.startswith("_")).delete()
    db(db.auth_user.email.startswith("_")).delete()
    num_test_users = db(db.user.username.startswith("_")).count()
    num_new_users = num_users - num_test_users
    print("Adding", num_new_users, "users.")
    for k in range(num_test_users, num_users):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = "_%s%.2i" % (first_name.lower(), k)
        user = dict(
            #username=username,
            email=username + "@ucsc.edu",
            first_name=first_name,
            last_name=last_name,
            password=username,  # To facilitate testing.
        )
        auth.register(user, send=False)
    
    a_users = db(db.auth_user).select()
    
    for a_u in a_users:
        username = "_%s%.2i" % (a_u.first_name.lower(), random.randint(1,21))
        profilePic = random.choice(
            ["profileTemplate.jpg", "profileTrees.jpg", "profileSammy.jpg", "profileSlug.jpg",
             "profileCampus.jpg"])
        category = random.choice(["rider", "driver"])
        numSeats = random.randint(2,5)
        carModel = random.choice(model)
        carMake = random.randint(2000,2022)
        location = random.choice(locationList)
        license = random.choice(nums) + random.choice(lets) + random.choice(lets) + random.choice(lets) + random.choice(nums) + random.choice(nums) + random.choice(nums)
        i = random.randint(0,6)
        schedule = random.choice(days_of_week) + ": " + r_times[i] + "-" + r_times[i+1]
        #temp data
        m = random.randint(0,6)
        monday = random.choice([r_times[m] + "-" + r_times[m+1], "None"])
        tu = random.randint(0,6)
        tuesday = random.choice([r_times[tu] + "-" + r_times[tu+1], "None"])
        w = random.randint(0,6)
        wednesday = random.choice([r_times[w] + "-" + r_times[w+1], "None"])
        th = random.randint(0,6)
        thursday = random.choice([r_times[th] + "-" + r_times[th+1], "None"])
        f = random.randint(0,6)
        friday = random.choice([r_times[f] + "-" + r_times[f+1], "None"])
        sa = random.randint(0,6)
        saturday = random.choice([r_times[sa] + "-" + r_times[sa+1], "None"])
        su = random.randint(0,6)
        sunday = random.choice([r_times[su] + "-" + r_times[su+1], "None"])

        user_info = dict(
            user_id = a_u.id,
            username=username,
            #email=username + "@ucsc.edu",
            firstName=a_u.first_name,
            lastName=a_u.last_name,
            password=username,  # To facilitate testing.
            category=category,
            numSeats=numSeats,
            carModel=carModel,
            carMake=carMake,
            location=location,
            license = license,
            schedule = schedule,
            profilePic = profilePic,

            #temporary database
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
        )
        #auth.register(user_info, send=False)
        # Adds some content for each user.
        db.user.insert(**user_info)

    
        
    users = db(db.user).select()
    for u in users:
        user_schedule = dict(
        user_id = u.id,
        day_of_week = random.choice(days_of_week),
        available_time = random.choice(r_times)  
        )
        db.user_schedule.insert(**user_schedule) 
       
       
    db.commit()

# def addUsersForTesting(num_users):
#     # Test user names begin with "_".
#     # Counts how many users we need to add.
#     db(db.auth_user.username.startswith("_")).delete()
#     num_test_users = db(db.auth_user.username.startswith("_")).count()
#     num_new_users = num_users - num_test_users
#     print("Adding", num_new_users, "users.")
#     for k in range(num_test_users, num_users):
#         first_name = random.choice(FIRST_NAMES)
#         last_name = random.choice(LAST_NAMES)
#         username = "_%s%.2i" % (first_name.lower(), k)
#         category = random.choice(["rider", "driver"])
#         numSeats = random.randint(2,5)
#         carModel = random.choice(model)
#         carMake = random.randint(2000,2022)
#         location = random.choice(locationList)
#         user_info = dict(
#             username=username,
#             #email=username + "@ucsc.edu",
#             firstName=first_name,
#             lastName=last_name,
#             password=username,  # To facilitate testing.
#             category=category,
#             numSeats=numSeats,
#             carModel=carModel,
#             carMake=carMake,
#             location=location
#         )
#         #auth.register(user_info, send=False)
#         # Adds some content for each user.
#         db.auth_user.insert(**user_info)
#     users = db(db.auth_user).select()
#     for u in users:
#         user_schedule = dict(
#         user_id = u.id,
#         day_of_week = random.choice(days_of_week),
#         available_time = random.choice(r_times)  
#         )
#         db.user_schedule.insert(**user_schedule) 
       
       
#     db.commit()
    

#adds the amount of mock users, the value can always be changed 
# addUsersForTesting(10)
add_users_for_testing(50)

#user schedule
db.define_table(
    'schedule',
    Field('created_by', 'reference auth_user', default=lambda: auth.user_id, readable=False, writable=False),
    Field('monday'),
    Field('tuesday'),
    Field('wednesday'),
    Field('thursday'),
    Field('friday'),
    Field('saturday'),
    Field('sunday'),
    Field('user_email', default=get_user_email),
)

db.schedule.id.readable = False
db.schedule.id.writable = False
db.schedule.user_email.readable = db.schedule.user_email.writable =False

db.define_table('stars',
                Field('image', 'reference auth_user'), 
                Field('rating', 'integer', default=0),
                Field('rater', 'reference auth_user', default=get_user) # User doing the rating.
                )
