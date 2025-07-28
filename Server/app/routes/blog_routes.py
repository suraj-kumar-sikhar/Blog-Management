from fastapi import APIRouter, HTTPException,Query
from app.models.blog import BlogBase, BlogResponse
from app.db.database import blogs_collection
from bson import ObjectId
from datetime import datetime
from bson.errors import InvalidId
from typing import Optional

router = APIRouter()

@router.get("", response_model=list[BlogResponse])
def get_all_approved_blogs(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None
):
    blogs = []
    query = {"approved": True}

    if category:
        query["category"] = category

    cursor = blogs_collection.find(query).sort("published", -1).skip(skip).limit(limit)
    for blog in cursor:
        blog["id"] = str(blog.pop("_id"))
        blog.setdefault("created_at", datetime.utcnow())
        blogs.append(BlogResponse(**blog))
    return blogs

@router.post("/create", response_model=BlogResponse)
def create_blog(blog: BlogBase):
    now = datetime.utcnow()
    blog_data = blog.model_dump()
    blog_data["created_at"] = now
    blog_data["updated_at"] = now

    result = blogs_collection.insert_one(blog_data)
    new_blog = blogs_collection.find_one({"_id": result.inserted_id})
    new_blog["id"] = str(new_blog.pop("_id"))
    return BlogResponse(**new_blog)

@router.get("/{id}", response_model=BlogResponse)
def get_blog_by_id(id: str):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid blog ID format")

    blog = blogs_collection.find_one({"_id": obj_id})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog["id"] = str(blog.pop("_id"))
    return BlogResponse(**blog)
