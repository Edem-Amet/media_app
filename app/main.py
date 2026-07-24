# Import necessary modules from FastAPI and other libraries
from fastapi import FastAPI

# Import models and database setup from respective modules
from . import models
from .database import engine
from .routers import post, user, auth


# Create all database tables based on the defined models
models.Base.metadata.create_all(bind=engine)


# Initialize the FastAPI application instance
app = FastAPI()

# Include routers to handle different endpoints
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Define a root endpoint that returns a welcome message
@app.get("/")
def root():
    return {"message": "Welcome to my Fast API"}


