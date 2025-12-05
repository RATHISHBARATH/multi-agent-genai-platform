
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from ..utils.security import fake_hash_password

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str):
    # placeholder auth - swap for real OAuth2/JWT in production
    if username == "admin" and fake_hash_password(password) == "hashed-secret":
        return {"access_token": "demo-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="invalid credentials")
