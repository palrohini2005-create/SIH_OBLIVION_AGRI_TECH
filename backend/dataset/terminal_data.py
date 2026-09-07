from mongodb import users_collection, officials_collection


def add_farmer():
    print("\n===== ADD FARMER =====")

    name = input("Farmer name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    password = input("Password: ")
    district = input("District: ")
    state = input("State: ")

    farmer = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "role": "farmer",
        "district": district,
        "state": state
    }

    result = users_collection.insert_one(farmer)

    print("\n✅ Farmer saved successfully!")
    print("MongoDB ID:", result.inserted_id)


def add_official():
    print("\n===== ADD OFFICIAL =====")

    name = input("Official name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    password = input("Password: ")
    designation = input("Designation: ")
    department = input("Department: ")
    district = input("District: ")
    state = input("State: ")

    official = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "role": "official",
        "designation": designation,
        "department": department,
        "district": district,
        "state": state
    }

    result = officials_collection.insert_one(official)

    print("\n✅ Official saved successfully!")
    print("MongoDB ID:", result.inserted_id)


while True:

    print("\n==============================")
    print("   FARMER & OFFICIAL DATABASE")
    print("==============================")
    print("1. Add Farmer")
    print("2. Add Official")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        add_farmer()

    elif choice == "2":
        add_official()

    elif choice == "3":
        print("Exiting...")
        break

    else:
        print("❌ Invalid choice")