from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .models.model_loader import load_llm, get_available_models
from .tools.story_generator import get_story_generator_tool
from .tools.summarizer import get_summary_tool
from app.tools.entity_extractor import get_entity_tool
from .tools.title_generator import get_title_generator_tool
from .tools.sentiment_analyzer import get_sentiment_tool
from .tools.theme_detector import get_theme_tool
from .tools.style_enhancer import get_style_enhancer_tool
from .cache.redis_cache import get_cache, set_cache
from .schemas import UserRegister, UserLogin, OTPVerify 
from .utils.ratelimiter import RateLimiter
from .database import users_collection
from .db_models import user_helper
from .utils.mail_utils import send_email_otp
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from jose import jwt 
import logging
import uuid
import time
import random
import pytz
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Story Generator API",
    description="Generate creative stories with customized parameters",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter
rate_limiter = RateLimiter(requests_per_minute=20)

class RequestBody(BaseModel):
    prompt: str
    genre: str
    tone: str
    style: Optional[str] = "No preference"
    story_length: Optional[str] = "Medium"
    include_twist: Optional[bool] = False
    protagonist_description: Optional[str] = None
    setting: Optional[str] = None
    model: Optional[str] = "default"  # Default model

class StoryResponse(BaseModel):
    request_id: str
    generated_text: str
    summary: str
    entities: List[str]
    title: str
    sentiment: Optional[dict] = None
    themes: Optional[List[str]] = None
    word_count: int
    processing_time: float

# Jobs queue for background processing
story_jobs = {}

# Load the default LLM
default_llm = load_llm()

# Function to get model based on user request
def get_model(model_name: str = "default"):
    if model_name == "default":
        return default_llm
    
    models = get_available_models()
    if model_name in models:
        return models[model_name]
    else:
        raise HTTPException(status_code=400, detail=f"Model {model_name} not available")
    
# Password Hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@app.post("/register/")
def register_user(user: UserRegister):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before storing
    hashed_password = hash_password(user.password)

    # Insert user into MongoDB
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password  # Store hashed password
    result = users_collection.insert_one(user_dict)

    # Retrieve inserted user and return response
    new_user = users_collection.find_one({"_id": result.inserted_id})
    return {"message": "User registered successfully", "user": user_helper(new_user)}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


BLOCK_TIME = 5  # Block time in minutes
IST = pytz.timezone("Asia/Kolkata")

@app.post("/login/")
async def login_user(user: UserLogin, background_tasks: BackgroundTasks):
    email = user.email
    now_utc = datetime.now(timezone.utc)

    # Fetch user from database
    existing_user = users_collection.find_one({"email": email})  # Use MongoDB query

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Check if user is blocked
    if existing_user.get("blocked_until"):
        blocked_until_utc = existing_user["blocked_until"]

        # Ensure timezone awareness
        if blocked_until_utc.tzinfo is None:
            blocked_until_utc = blocked_until_utc.replace(tzinfo=timezone.utc)

        blocked_until_ist = blocked_until_utc.astimezone(IST)

        if now_utc < blocked_until_utc:
            raise HTTPException(
                status_code=403, 
                detail=f"Too many failed attempts. Try again at {blocked_until_ist.strftime('%Y-%m-%d %H:%M:%S')} IST."
            )

    # Verify password
    if not verify_password(user.password, existing_user["password"]):
        failed_attempts = existing_user.get("failed_attempts", 0) + 1

        if failed_attempts >= 3:
            blocked_until_utc = now_utc + timedelta(minutes=BLOCK_TIME)
            users_collection.update_one(
                {"email": email}, 
                {"$set": {"failed_attempts": failed_attempts, "blocked_until": blocked_until_utc}}
            )
            blocked_until_ist = blocked_until_utc.astimezone(IST)
            raise HTTPException(
                status_code=403, 
                detail=f"Too many failed attempts. Try again at {blocked_until_ist.strftime('%Y-%m-%d %H:%M:%S')} IST."
            )
        else:
            users_collection.update_one(
                {"email": email}, 
                {"$set": {"failed_attempts": failed_attempts}}
            )
            raise HTTPException(status_code=400, detail="Invalid credentials")

    # Reset failed attempts on successful login
    users_collection.update_one(
        {"email": email}, 
        {"$set": {"failed_attempts": 0, "blocked_until": None}}
    )

    # Generate and store OTP in MongoDB
    otp = str(random.randint(100000, 999999))
    users_collection.update_one(
        {"email": email}, 
        {"$set": {"otp": otp, "otp_created_at": now_utc}}
    )

    print(f"Stored OTP for {email}: {otp}")  # Debugging output

    # Send OTP via Email
    background_tasks.add_task(send_email_otp, email, otp)

    return {"message": "OTP sent to your email. Please verify to continue"}


SECRET_KEY = "19022d375641eb6926d9395e6492b958e372dce116cfac4c926830cd01e2f18f"  # Change this to a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAY = 7  # 1 days

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/verify-otp/")
async def verify_otp(otp_data: OTPVerify):
    email = otp_data.email
    otp = otp_data.otp

    # Fetch user from database
    existing_user = users_collection.find_one({"email": email})

    if not existing_user or "otp" not in existing_user or existing_user["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Generate JWT Token (dummy for now)
    access_token = create_access_token({"sub": otp_data.email})

    # Remove OTP from database after successful verification
    users_collection.update_one(
        {"email": email}, 
        {"$unset": {"otp": "", "otp_created_at": ""}}
    )

    return {"message": "Login successful", "access_token": access_token}


@app.get("/models")
def list_available_models():
    """Get a list of available language models"""
    models = get_available_models()
    return {"models": list(models.keys())}

@app.post("/generate/")
async def generate(body: RequestBody, background_tasks: BackgroundTasks):
    """Generate a story based on the provided parameters"""
    # Apply rate limiting
    if not rate_limiter.allow_request():
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"story:{body.prompt[:50]}:{body.genre}:{body.tone}"
        cached_result = get_cache(cache_key)
        
        if cached_result:
            logger.info(f"Cache hit for request {request_id}")
            return {**cached_result, "request_id": request_id, "cached": True}
        
        # Get the requested model
        llm = get_model(body.model)
        
        # Initialize tools with the chosen model
        tools = [
            get_story_generator_tool(llm),
            get_summary_tool(),
            get_entity_tool(),
            get_title_generator_tool(llm),
            get_sentiment_tool(),
            get_theme_tool(),
            get_style_enhancer_tool(llm),
        ]
        
        # Process story generation
        story_msg = tools[0].func({
            "prompt": body.prompt,
            "genre": body.genre,
            "tone": body.tone,
            "style": body.style,
            "story_length": body.story_length,
            "include_twist": body.include_twist,
            "protagonist_description": body.protagonist_description,
            "setting": body.setting
        })
        story = story_msg.content
        
        # Process additional story information in parallel
        summary = tools[1].func(story)
        entities = tools[2].func(story)
        title_msg = tools[3].func(story)
        title = title_msg.content.strip()
        
        # Additional analysis (can be done in background)
        sentiment = tools[4].func(story)
        themes = tools[5].func(story)
        
        # Optional style enhancement
        if body.style != "No preference":
            enhanced_story_msg = tools[6].func({
                "story": story,
                "style": body.style
            })
            story = enhanced_story_msg.content
        
        # Calculate processing time and word count
        processing_time = time.time() - start_time
        word_count = len(story.split())
        
        # Prepare response
        result = {
            "request_id": request_id,
            "generated_text": story,
            "summary": summary,
            "entities": entities,
            "title": title,
            "sentiment": sentiment,
            "themes": themes,
            "word_count": word_count,
            "processing_time": processing_time
        }
        
        # Cache the result (except for very specific prompts)
        if len(body.prompt) < 200:  # Only cache shorter prompts
            set_cache(cache_key, result, expire=3600)  # Cache for 1 hour
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

@app.post("/generate/async/")
async def generate_async(body: RequestBody, background_tasks: BackgroundTasks):
    """Generate a story asynchronously for longer generations"""
    # Apply rate limiting
    if not rate_limiter.allow_request():
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    
    # Add job to queue
    story_jobs[request_id] = {"status": "pending", "created_at": time.time()}
    
    # Start background task
    background_tasks.add_task(process_story_async, request_id, body)
    
    return {"request_id": request_id, "status": "pending"}

async def process_story_async(request_id: str, body: RequestBody):
    """Process a story generation request asynchronously"""
    try:
        # Mark job as processing
        story_jobs[request_id]["status"] = "processing"
        
        # Similar processing as in the synchronous endpoint
        llm = get_model(body.model)
        
        # Initialize tools
        tools = [
            get_story_generator_tool(llm),
            get_summary_tool(),
            get_entity_tool(),
            get_title_generator_tool(llm),
        ]
        
        # Process story
        story_msg = tools[0].func({
            "prompt": body.prompt,
            "genre": body.genre,
            "tone": body.tone,
            "style": body.style,
            "story_length": body.story_length,
            "include_twist": body.include_twist
        })
        story = story_msg.content
        
        # Process additional story information
        summary = tools[1].func(story)
        entities = tools[2].func(story)
        title_msg = tools[3].func(story)
        title = title_msg.content.strip()
        
        # Save result
        story_jobs[request_id] = {
            "status": "completed",
            "generated_text": story,
            "summary": summary,
            "entities": entities,
            "title": title,
            "completed_at": time.time()
        }
    except Exception as e:
        logger.error(f"Error in async job {request_id}: {str(e)}")
        story_jobs[request_id] = {
            "status": "failed",
            "error": str(e),
            "completed_at": time.time()
        }

@app.get("/job/{request_id}")
async def get_job_status(request_id: str):
    """Get the status of an asynchronous job"""
    if request_id not in story_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = story_jobs[request_id]
    
    # Clean up completed jobs after 1 hour
    if job["status"] in ["completed", "failed"]:
        if "completed_at" in job and (time.time() - job["completed_at"]) > 3600:
            # Keep the job in the response but remove it from memory
            result = job.copy()
            del story_jobs[request_id]
            return result
    
    return job

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "active_jobs": len([j for j in story_jobs.values() if j["status"] == "processing"]),
        "queue_size": len([j for j in story_jobs.values() if j["status"] == "pending"])
    }

# Cleanup task to remove old jobs
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_jobs())

async def cleanup_old_jobs():
    while True:
        try:
            current_time = time.time()
            to_remove = []
            
            for job_id, job in story_jobs.items():
                # Remove completed/failed jobs older than 1 hour
                if job["status"] in ["completed", "failed"] and "completed_at" in job:
                    if (current_time - job["completed_at"]) > 3600:
                        to_remove.append(job_id)
                
                # Remove pending jobs older than 6 hours
                elif job["status"] == "pending" and (current_time - job["created_at"]) > 21600:
                    to_remove.append(job_id)
            
            # Remove the identified jobs
            for job_id in to_remove:
                del story_jobs[job_id]
                
            # Sleep for 10 minutes before checking again
            await asyncio.sleep(600)
        except Exception as e:
            logger.error(f"Error in cleanup task: {str(e)}")
            await asyncio.sleep(60)  # Retry after a minute