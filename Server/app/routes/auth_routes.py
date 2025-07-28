from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from bson import ObjectId
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD, JWT_SECRET
from app.db.database import blogs_collection
from app.models.blog import BlogResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class Token(BaseModel):
    access_token: str
    token_type: str


class BlogUpdate(BaseModel):
    title: str
    author: str
    category: str
    content: str


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != ADMIN_USERNAME:
            raise HTTPException(status_code=401, detail="Invalid admin credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != ADMIN_USERNAME or form_data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(
        data={"sub": ADMIN_USERNAME},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/dashboard", response_model=list[BlogResponse])
def get_all_blogs(token: str = Depends(verify_token)):
    blogs = []
    for blog in blogs_collection.find():
        blog["id"] = str(blog.pop("_id"))
        blogs.append(BlogResponse(**blog))
    return blogs


@router.put("/dashboard/{id}")
def update_blog(id: str, updated_data: BlogUpdate, token: str = Depends(verify_token)):
    result = blogs_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog updated successfully"}


@router.put("/dashboard/{id}/approve")
def approve_blog(id: str, token: str = Depends(verify_token)):
    result = blogs_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"approved": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog approved"}


@router.delete("/dashboard/{id}")
def delete_blog(id: str, token: str = Depends(verify_token)):
    result = blogs_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted"}
