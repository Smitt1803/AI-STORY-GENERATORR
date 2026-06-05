from bson import ObjectId

def user_helper(user) -> dict:
    return {
        "_id": str(user["_id"]),  # Convert ObjectId to string
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],  # Hashed password
        # "profile_image": user.get("profile_image", None)
        "failed_attempts": user.get("failed_attempts", 0),
        "blocked_until": user.get("blocked_until", None),
    }