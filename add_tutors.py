from pymongo import MongoClient

# Replace <connection_string> with your actual connection string
connection_string = "mongodb+srv://kumawatr:JhvogRcEEo10IHyI@cluster9.2bjhi.mongodb.net/"  # e.g., "mongodb+srv://<username>:<password>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(connection_string)

# Select your database
db = client['tutouring-platform']  # Your actual database name

# Select the tutors collection
tutors_collection = db['tutors']  # Your actual collection name

# Example tutor data
tutors_data = [
    {
        'name': 'Alice Johnson',
        'subject': 'Mathematics',
        'availability': 'Mon-Fri, 5 PM - 8 PM',
        'rate': 30,
        'years_of_experience': 5
    },
    {
        'name': 'Bob Smith',
        'subject': 'Science',
        'availability': 'Sat-Sun, 10 AM - 2 PM',
        'rate': 25,
        'years_of_experience': 4
    },
    {
        'name': 'Charlie Brown',
        'subject': 'English',
        'availability': 'Mon-Fri, 6 PM - 9 PM',
        'rate': 35,
        'years_of_experience': 6
    }
]

# Insert tutor data into the collection
result = tutors_collection.insert_many(tutors_data)

# Print the inserted IDs
print("Tutors added with IDs:", result.inserted_ids)
