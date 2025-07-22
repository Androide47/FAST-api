from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str 
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        role=create_user_request.role
    )

    db.add(create_user_model)
    db.commit()

    if create_user_model is not None:
        return create_user_model
    raise HTTPException(status_code=400, detail="User creation failed.")

@router.post("/token")
async def login_for_access_token():
    return 'token'