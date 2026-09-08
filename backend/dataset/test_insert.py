from mongodb import users_collection

farmer = {
    "name": "Ramesh Patil",
    "email": "ramesh@gmail.com",
    "phone": "9876543210",
    "role": "farmer",
    "district": "Nashik",
    "state": "Maharashtra"
}

result = users_collection.insert_one(farmer)

print("✅ Farmer saved successfully!")
print("MongoDB ID:", result.inserted_id)