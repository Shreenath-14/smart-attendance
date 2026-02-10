import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

MONGO_URI = "mongodb://127.0.0.1:27017"
DB_NAME = "smart_attendance"

# Match the project's hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_demo_user():
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    users = db.users
    teachers = db.teachers

    email = "teacher@gmail.com"
    
    # Check if exists and cleanup
    existing = await users.find_one({"email": email})
    if existing:
        print(f"User {email} already exists. Deleting to recreate...")
        await users.delete_one({"_id": existing["_id"]})
        # Remove associated teacher profile if exists
        await teachers.delete_one({"userId": existing["_id"]})

    print("Creating demo user...")
    password_hash = pwd_context.hash("teacher123")
    
    user_doc = {
        "name": "Teacher User",
        "email": email,
        "password_hash": password_hash,
        "role": "teacher",
        "college_name": "Demo College",
        "is_verified": True,
        "created_at": datetime.utcnow()
    }
    
    result = await users.insert_one(user_doc)
    user_id = result.inserted_id
    print(f"User created with ID: {user_id}")
    
    with open("demo_user_id.txt", "w") as f:
        f.write(str(user_id))

    print("Creating teacher profile...")
    teacher_doc = {
        "userId": user_id,
        "employee_id": "EMP001",
        "college_name": "Demo College",
        "phone": "1234567890",
        "branch": "CSE",
        "subjects": [],
        "avatarUrl": None,
        "department": "Computer Science",
        "settings": {
            "theme": "Light",
            "notifications": {
                "push": True,
                "inApp": True,
                "sound": False,
            },
             "faceSettings": {
                "sensitivity": 80,
                "liveness": True,
            },
        },
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
    
    await teachers.insert_one(teacher_doc)
    print("Teacher profile created.")
    print("------------------------------------------------")
    print("Demo User Credentials:")
    print(f"Email: {email}")
    print("Password: teacher123")
    print("------------------------------------------------")
    
    client.close()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_demo_user())
