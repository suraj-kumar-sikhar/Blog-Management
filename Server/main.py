from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import blog_routes,auth_routes # optional

app = FastAPI(
    title="Blog Management API",
    description="API for managing blog posts with admin approval.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

app.include_router(blog_routes.router, prefix="/api/blogs", tags=["Blogs"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
