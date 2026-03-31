import os   #environment variable management
from pathlib import Path  #handling file paths
from enum import Enum     #for creating enumerations
from dotenv import load_dotenv   #for loading environment variables from .env file
from fastapi import FastAPI, HTTPException, Depends, Request, Path as FastPath   #for building the API and handling requests
from fastapi.security import HTTPBearer    #for handling HTTP Bearer authentication
import time   #for handling time-based operations like rate limiting
from fastapi.responses import PlainTextResponse  #for returning plain text responses
# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent  
env_path = BASE_DIR / '.env'    
load_dotenv(dotenv_path=env_path)   # Load environment variables from the .env file.
from app.services import generate_market_report  #importing the function to generate market report
from app.utils import fetch_market_news    #importing the function to fetch market news
from app.auth import create_access_token, verify_jwt   #importing the functions for JWT token creation and verification

app = FastAPI(title="Trade Opportunities API (JWT Secured)")    #initializing the app with a title
usage_history = {}  # to track usage per IP for rate limiting
security = HTTPBearer()  # initialize security for JWT authentication
rate_limit_store = {}   # to track request timestamps for rate limiting
RATE_LIMIT_MAX = 5     # Maximum requests allowed
WINDOW_SECONDS = 60    # Time window in seconds


# this function is for the check the rate limit for each IP address, and also if the limit is exceeded, it will return 429 error.
async def check_rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()
    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip] if now - t < WINDOW_SECONDS
    ]    
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_MAX} requests per minute."
        )    
    rate_limit_store[client_ip].append(now)
    return len(rate_limit_store[client_ip])


# this class for validating the sector name.
class SectorName(str, Enum):
    pharmaceuticals = "pharmaceuticals"
    technology = "technology"
    agriculture = "agriculture"

# this function is for the login and get the token for the user.
@app.post("/token")
async def login(api_key: str):
    if api_key != os.getenv("SECRET_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    access_token = create_access_token(data={"sub": "appscrip_user"})
    return {"access_token": access_token, "token_type": "bearer"}


# this function is for the analyze the sector and get the market report for the sector..
@app.get("/analyze/{sector}", response_class=PlainTextResponse) 
async def analyze_sector(
    sector: SectorName, 
    request: Request, 
    token_data=Depends(verify_jwt),
    current_count: int = Depends(check_rate_limit)
):
    client_ip = request.client.host
    usage_history[client_ip] = usage_history.get(client_ip, 0) + 1
    try:
        raw_data = await fetch_market_news(sector.value)
        report = await generate_market_report(sector.value, raw_data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))