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
