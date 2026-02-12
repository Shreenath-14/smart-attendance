import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def seed():
    # Connect
    uri = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(uri)
    db = client["smart-attendance"]

    logger.info("Seeding database...")

    # --- Seed Student ---
    student_email = "student@gmail.com"
    student_pass = "student123"  # nosec

    existing_student = await db.users.find_one({"email": student_email})
    if not existing_student:
        logger.info(f"Creating student: {student_email}")
        user_doc = {
            "name": "Demo Student",
            "email": student_email,
            "password_hash": hash_password(student_pass),
            "role": "student",
            "college_name": "Demo University",
            "is_verified": True,
            "verification_token": None,
            "created_at": datetime.now(timezone.utc),
        }
        res = await db.users.insert_one(user_doc)

        student_profile = {
            "userId": res.inserted_id,
            "name": "Demo Student",
            "email": student_email,
            "college_name": "Demo University",
            "branch": "Computer Science",
            "roll": "CS101",
            "year": "3rd Year",
            "created_at": datetime.now(timezone.utc),
        }
        await db.students.insert_one(student_profile)
    else:
        logger.info(f"Student {student_email} already exists.")

    # --- Seed Teacher ---
    teacher_email = "teacher@gmail.com"
    teacher_pass = "teacher123"  # nosec

    existing_teacher = await db.users.find_one({"email": teacher_email})
    if not existing_teacher:
        logger.info(f"Creating teacher: {teacher_email}")
        user_doc = {
            "name": "Demo Teacher",
            "email": teacher_email,
            "password_hash": hash_password(teacher_pass),
            "role": "teacher",
            "college_name": "Demo University",
            "is_verified": True,
            "verification_token": None,
            "created_at": datetime.now(timezone.utc),
        }
        res = await db.users.insert_one(user_doc)

        teacher_profile = {
            "userId": res.inserted_id,
            "name": "Demo Teacher",
            "email": teacher_email,
            "college_name": "Demo University",
            "employee_id": "EMP001",
            "phone": "1234567890",
            "created_at": datetime.now(timezone.utc),
        }
        await db.teachers.insert_one(teacher_profile)
    else:
        logger.info(f"Teacher {teacher_email} already exists.")

    # --- Seed Subjects (Create if not exist) ---
    student_user = await db.users.find_one({"email": student_email})
    student_doc = await db.students.find_one({"userId": student_user["_id"]})
    teacher_user = await db.users.find_one({"email": teacher_email})
    teacher_doc = await db.teachers.find_one({"userId": teacher_user["_id"]})

    subjects_data = [
        {"name": "Mathematics", "code": "MTH101", "type": "Core"},
        {"name": "Physics", "code": "PHY101", "type": "Lab"},
        {"name": "Chemistry", "code": "CHM101", "type": "Theory"},
        {"name": "Computer Science", "code": "CS101", "type": "Elective"}
    ]

    for sub in subjects_data:
        existing_sub = await db.subjects.find_one({"code": sub["code"]})
        if not existing_sub:
             logger.info(f"Creating subject: {sub['name']}")
             
             # Create subject with enrollment
             sub_doc = {
                 "name": sub["name"],
                 "code": sub["code"],
                 "type": sub["type"],
                 "professor_ids": [teacher_doc["_id"]],
                 "students": [
                     {
                         "student_id": student_doc["_id"],
                         "name": student_user["name"],
                         "verified": True,
                         "attendance": {
                             "present": 20,
                             "absent": 5,
                             "total": 25,
                             "percentage": 80.0
                         }
                     }
                 ],
                 "created_at": datetime.now(timezone.utc)
             }
             res = await db.subjects.insert_one(sub_doc)
             sub_id = res.inserted_id

             # Update Student with subject
             await db.students.update_one(
                 {"_id": student_doc["_id"]},
                 {"$addToSet": {"subjects": sub_id}}
             )
             
             # Update Teacher with subject
             await db.teachers.update_one(
                 {"_id": teacher_doc["_id"]},
                 {"$addToSet": {"subjects": sub_id}}
             )
        else:
            logger.info(f"Subject {sub['name']} already exists.")


    logger.info("Seeding complete!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
