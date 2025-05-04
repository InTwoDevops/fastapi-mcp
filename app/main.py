from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from fastapi_mcp import FastApiMCP

# Improved API metadata
app = FastAPI(
    title="Reminders API",
    description="A simple API for managing reminders with CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

mcp = FastApiMCP(app)

mcp.mount()

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb://mongodb:27017")
    app.mongodb = app.mongodb_client["reminders_db"]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Pydantic models
class ReminderBase(BaseModel):
    title: str = Field(..., description="The title of the reminder", example="Buy groceries")
    description: Optional[str] = Field(None, description="Detailed description of the reminder", example="Milk, eggs, bread")
    due_date: Optional[datetime] = Field(None, description="Due date for the reminder", example="2023-12-31T12:00:00")

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the reminder")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the reminder was created")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "due_date": "2023-12-31T12:00:00",
                "created_at": "2023-12-01T09:30:00"
            }
        }

# Root endpoint with API info
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic API information and available endpoints.
    """
    return {
        "app": "Reminders API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "create_reminder": "POST /reminders/",
            "get_all_reminders": "GET /reminders/",
            "get_reminder": "GET /reminders/{reminder_id}",
            "update_reminder": "PUT /reminders/{reminder_id}",
            "delete_reminder": "DELETE /reminders/{reminder_id}"
        }
    }

# CRUD operations with improved documentation
@app.post(
    "/reminders/", 
    response_model=Reminder, 
    status_code=status.HTTP_201_CREATED,
    tags=["Reminders"],
    summary="Create a new reminder",
    description="Create a new reminder with the provided title, optional description, and optional due date."
)
async def create_reminder(reminder: ReminderCreate):
    """
    Create a new reminder with the following parameters:
    
    - **title**: Required title of the reminder
    - **description**: Optional description with details
    - **due_date**: Optional date when the reminder is due
    
    Returns the created reminder with generated ID and creation timestamp.
    """
    new_reminder = Reminder(
        title=reminder.title,
        description=reminder.description,
        due_date=reminder.due_date
    )
    await app.mongodb["reminders"].insert_one(new_reminder.model_dump())
    return new_reminder

@app.get(
    "/reminders/", 
    response_model=List[Reminder],
    tags=["Reminders"],
    summary="Get all reminders",
    description="Retrieve a list of all reminders stored in the database."
)
async def read_reminders():
    """
    Retrieve all reminders.
    
    Returns a list of all reminders in the database (limited to 1000 entries).
    """
    reminders = await app.mongodb["reminders"].find().to_list(1000)
    return reminders

@app.get(
    "/reminders/{reminder_id}", 
    response_model=Reminder,
    tags=["Reminders"],
    summary="Get a specific reminder",
    description="Retrieve a specific reminder by its ID."
)
async def read_reminder(reminder_id: str):
    """
    Retrieve a specific reminder by ID.
    
    - **reminder_id**: The unique identifier of the reminder
    
    Returns the reminder if found, otherwise raises a 404 error.
    """
    reminder = await app.mongodb["reminders"].find_one({"id": reminder_id})
    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Reminder with ID {reminder_id} not found"
        )
    return reminder

@app.put(
    "/reminders/{reminder_id}", 
    response_model=Reminder,
    tags=["Reminders"],
    summary="Update a reminder",
    description="Update an existing reminder by its ID with new data."
)
async def update_reminder(reminder_id: str, reminder: ReminderBase):
    """
    Update a specific reminder by ID.
    
    - **reminder_id**: The unique identifier of the reminder to update
    - **reminder**: The updated reminder data
    
    Returns the updated reminder if found, otherwise raises a 404 error.
    """
    update_result = await app.mongodb["reminders"].update_one(
        {"id": reminder_id},
        {"$set": reminder.model_dump()}
    )
    
    if update_result.modified_count == 0:
        reminder_exists = await app.mongodb["reminders"].find_one({"id": reminder_id})
        if not reminder_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Reminder with ID {reminder_id} not found"
            )
        
    updated_reminder = await app.mongodb["reminders"].find_one({"id": reminder_id})
    return updated_reminder

@app.delete(
    "/reminders/{reminder_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Reminders"],
    summary="Delete a reminder",
    description="Delete an existing reminder by its ID."
)
async def delete_reminder(reminder_id: str):
    """
    Delete a specific reminder by ID.
    
    - **reminder_id**: The unique identifier of the reminder to delete
    
    Returns no content (204) if successful, otherwise raises a 404 error.
    """
    delete_result = await app.mongodb["reminders"].delete_one({"id": reminder_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Reminder with ID {reminder_id} not found"
        )
    return None 

mcp.setup_server()