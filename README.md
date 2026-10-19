Budget Travel Planner API
COM661 Full Stack Strategies and Development - CW1 (Back End)
About the project
This is my back-end coursework project for COM661. The API helps travellers find places to visit in London, organise their trips and keep track of their spending.

Users can look for attractions within their budget, save a plan for each day and record expenses during their trip. The budget overview brings their planned costs and actual spending together so they can see how much money they have left.
Main features
- View attraction details, including locations, entry costs and travel tips.
- Filter attractions by price, including free places.
- Create, view, edit and delete trips and itinerary stops.
- Record and manage expenses for accommodation, food, transport and attractions.
- Compare planned costs with actual spending and check the remaining budget.
- Log in and log out.
Tools used
- Python and Flask for the API, with routes organised into Blueprints.
- MongoDB and PyMongo for storing and accessing the data.
- JWT for authentication and bcrypt for hashing passwords.
- A token blacklist to invalidate tokens when users log out.
- Postman for running API requests and automated tests.
Dataset
The database contains three main collections:
- users: 10 test users, including one administrator.
- attractions: 100 London attraction records. Each record contains nested details for its location, prices, opening hours, facilities, travel tips, reviews and events.
- trips: 30 sample trips, each containing itinerary stops and expenses.
The starting attraction list is stored in attractions_base.json. The travelData.py script builds the full dataset. The setup_database.py script then loads it into MongoDB and creates the indexes.
Running the project
These commands are for macOS or Linux. Before starting, make sure Python 3 is installed, MongoDB is running or reachable, and the project's database connection settings match your MongoDB instance.

Open a terminal in the travelBE project folder.
1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
2. Install the required packages
python -m pip install -r requirements.txt
3. Prepare the dataset and database
For the initial setup, run:
python travelData.py
python setup_database.py
4. Start the API
python app.py
The API runs at http://127.0.0.1:5001. Keep this terminal running while using Postman.
Test accounts
These accounts are for local coursework testing:
Account	Username	Password
Administrator	admin	admin_pw
Regular user	sara	sara_pw


API structure
The API has 37 endpoints organised into seven Blueprints:
- auth: login and logout.
- attractions: attraction details, searches and filters.
- reviews: attraction reviews.
- events: events linked to attractions.
- trips: saved trips and budget calculations.
- stops: stops within a trip's itinerary.
- expenses: spending recorded against a trip.
Testing with Postman
1. Start the API using python app.py.
2. Open Postman and import Budget_Travel_Planner.postman_collection.json.
3. Check that the requests use the local API address shown above.
4. Run the collection and review the responses and test results.
Use of AI
I used an AI assistant for support during development. The related chat history is included in my Design and Development document.
