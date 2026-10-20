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

# ---------------- ATTRACTIONS ----------------

def generate_attractions(user_list):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    tips = ['Arrive early to avoid queues.', 'Weekday mornings are the quietest.',
            'Book tickets online to save money.', 'Check the website for free events.',
            'Use contactless on the Tube to travel cheaply.', 'It is a short walk from the station.',
            'Ask at the entrance about step-free routes.']

    review_comments = ['Absolutely loved it, would go again.', 'Really good, just a bit busy.',
                       'Great day out, worth the trip.', 'It was okay, nothing special.',
                       'Too crowded and hard to see much.', 'Expected more for the price.',
                       'Perfect for families.', 'Would not recommend.']

    event_types = ['talk', 'tour', 'workshop', 'festival']
    event_titles = {'talk': ['Curator talk', 'History talk'],
                    'tour': ['Evening tour', 'Behind the scenes tour'],
                    'workshop': ['Family workshop', 'Drawing workshop'],
                    'festival': ['Christmas festival', 'Food festival']}

    # only normal users write reviews, not the admin
    normal_users = []
    for user in user_list:
        if user['role'] == 'user':
            normal_users.append(user)

    # the 100 real London places
    with open('attractions_base.json') as fin:
        places = json.load(fin)

    attraction_list = []

    for place in places:
        adult_price = place['adult_price']

        # opening hours: free parks, markets and landmarks are open all day
        opening_hours = []
        for day in days:
            if adult_price == 0 and place['category'] in ['park', 'market', 'landmark']:
                open_time = '07:00'
                close_time = '21:00'
            else:
                open_time = random.choice(['09:00', '10:00'])
                close_time = random.choice(['17:00', '17:30', '18:00'])
            opening_hours.append({'day': day, 'open': open_time, 'close': close_time})

        # reviews: random.sample picks DIFFERENT people,
        # so nobody reviews the same place twice
        reviews = []
        reviewers = random.sample(normal_users, random.randint(2, 5))
        for user in reviewers:
            reviews.append({
                '_id': make_id(),
                'user_id': user['_id'],
                'username': user['username'],
                'ratings': {
                    'overall': random.randint(1, 5),
                    'value_for_money': random.randint(1, 5),
                    'accessibility': random.randint(1, 5)
                },
                'comment': random.choice(review_comments),
                'visit_date': make_date('2026-08-' + str(random.randint(10, 28))),
                'created_at': make_date('2026-09-' + str(random.randint(10, 28)))
            })

        # events: some places have none, some have one or two
        events = []
        for _ in range(random.randint(0, 2)):
            event_type = random.choice(event_types)
            start_day = random.randint(10, 25)
            end_day = start_day + random.randint(0, 3)
            events.append({
                '_id': make_id(),
                'title': random.choice(event_titles[event_type]),
                'type': event_type,
                'start_date': make_date('2026-12-' + str(start_day)),
                'end_date': make_date('2026-12-' + str(end_day)),
                'price': random.choice([0, 0, 5, 10, 15]),
                'booking_required': random.choice([True, False])
            })

        attraction_list.append({
            '_id': make_id(),
            'name': place['name'],
            'description': place['description'],
            'category': place['category'],
            'tags': place['tags'],
            'location': {
                'address': place['area'] + ', London',
                'area': place['area'],
                'postcode': place['postcode'],
                'nearest_station': place['nearest_station'],
                # GeoJSON point - MongoDB wants longitude first, then latitude
                'coordinates': {
                    'type': 'Point',
                    'coordinates': [place['longitude'], place['latitude']]
                }
            },
            'entry_cost_gbp': {
                'adult': adult_price,
                'child': round(adult_price * 0.5, 2),
                'concession': round(adult_price * 0.8, 1),
                'is_free': adult_price == 0
            },
            'opening_hours': opening_hours,
            'facilities': {
                'step_free': random.choice([True, False]),
                'cafe': random.choice([True, False]),
                'toilets': True
            },
            'travel_tips': random.sample(tips, 2),
            'reviews': reviews,
            'events': events
        })

    return attraction_list
