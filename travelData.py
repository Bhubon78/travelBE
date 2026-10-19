import random
import json
import bcrypt
from bson import ObjectId


# JSON has no date or ObjectId type, so I write them in MongoDB's own format.
# When I use mongoimport, these become a real date and a real ObjectId.
def make_date(text):
    return {'$date': text + 'T00:00:00Z'}

def make_id():
    return {'$oid': str(ObjectId())}


# ---------------- USERS ----------------

def generate_users():
    names = ['Admin User', 'Sara Khan', 'Tom Reid', 'Aisha Patel', 'James Murphy',
             'Mei Chen', 'Daniel Okafor', 'Laura Smith', 'Omar Hassan', 'Emily Jones']

    usernames = ['admin', 'sara', 'tom', 'aisha', 'james',
                 'mei', 'daniel', 'laura', 'omar', 'emily']

    user_list = []

    for i in range(10):
        name = names[i]
        username = usernames[i]

        # everyone's password is their username + _pw, e.g. sara_pw
        password = username + '_pw'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if username == 'admin':
            role = 'admin'
        else:
            role = 'user'

        user_list.append({
            '_id': make_id(),
            'name': name,
            'username': username,
            'email': username + '@example.com',
            'password_hash': password_hash.decode('utf-8'),
            'role': role,
            'created_at': make_date('2026-09-' + str(random.randint(10, 28)))
        })

    return user_list

