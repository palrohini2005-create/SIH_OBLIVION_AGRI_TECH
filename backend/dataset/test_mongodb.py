from mongodb import client

try:
    client.admin.command("ping")
    print("✅ MongoDB Atlas connected successfully!")

except Exception as e:
    print("❌ MongoDB connection failed:")
    print(e)