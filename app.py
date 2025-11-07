"""FastAPI Backend Application

A comprehensive backend service with FastAPI providing:
- RESTful API endpoints
- Health checks
- CORS middleware
- Data validation with Pydantic
- Error handling
- Documentation auto-generation
"""

from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="AB SDLC Agent AI Backend",
    description="Backend API for SDLC Agent AI system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskPriority(str, Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Pydantic Models
class TaskBase(BaseModel):
    """Base task model"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Task priority")
    assignee: Optional[str] = Field(None, max_length=100, description="Assigned user")
    tags: Optional[List[str]] = Field(default_factory=list, description="Task tags")

    @validator('tags')
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v

class TaskCreate(TaskBase):
    """Task creation model"""
    pass

class TaskUpdate(BaseModel):
    """Task update model - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None

class Task(TaskBase):
    """Complete task model with system fields"""
    id: int = Field(..., description="Task ID")
    status: TaskStatus = Field(TaskStatus.PENDING, description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Implement authentication",
                "description": "Add JWT-based authentication to the API",
                "status": "in_progress",
                "priority": "high",
                "assignee": "john.doe",
                "tags": ["backend", "security"],
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }

class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")

class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=8, description="Password")

class User(UserBase):
    """Complete user model"""
    id: int = Field(..., description="User ID")
    is_active: bool = Field(True, description="User active status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "created_at": "2024-01-01T12:00:00"
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    service: str

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    timestamp: datetime
    path: Optional[str] = None

# In-memory data storage (replace with database in production)
tasks_db: Dict[int, Task] = {}
users_db: Dict[int, User] = {}
task_counter = 0
user_counter = 0

# Helper functions
def get_next_task_id() -> int:
    """Generate next task ID"""
    global task_counter
    task_counter += 1
    return task_counter

def get_next_user_id() -> int:
    """Generate next user ID"""
    global user_counter
    user_counter += 1
    return user_counter

# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AB SDLC Agent AI Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "tasks": "/api/v1/tasks",
            "users": "/api/v1/users"
        }
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        service="ab-sdlc-agent-ai-backend"
    )

# Task endpoints
@app.post(
    "/api/v1/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task"
)
async def create_task(task_data: TaskCreate) -> Task:
    """Create a new task"""
    task_id = get_next_task_id()
    task = Task(
        id=task_id,
        **task_data.model_dump(),
        status=TaskStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    tasks_db[task_id] = task
    return task

@app.get(
    "/api/v1/tasks",
    response_model=List[Task],
    tags=["Tasks"],
    summary="Get all tasks"
)
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
) -> List[Task]:
    """Get all tasks with optional filtering and pagination"""
    tasks = list(tasks_db.values())
    
    # Apply filters
    if status:
        tasks = [t for t in tasks if t.status == status]
    if priority:
        tasks = [t for t in tasks if t.priority == priority]
    if assignee:
        tasks = [t for t in tasks if t.assignee == assignee]
    
    # Apply pagination
    return tasks[skip:skip + limit]

@app.get(
    "/api/v1/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Get a specific task"
)
async def get_task(task_id: int = Path(..., gt=0, description="Task ID")) -> Task:
    """Get a task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return tasks_db[task_id]

@app.put(
    "/api/v1/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Update a task"
)
async def update_task(
    task_id: int = Path(..., gt=0, description="Task ID"),
    task_update: TaskUpdate = ...
) -> Task:
    """Update a task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    task = tasks_db[task_id]
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Update fields
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    tasks_db[task_id] = task
    return task

@app.patch(
    "/api/v1/tasks/{task_id}/status",
    response_model=Task,
    tags=["Tasks"],
    summary="Update task status"
)
async def update_task_status(
    task_id: int = Path(..., gt=0, description="Task ID"),
    new_status: TaskStatus = Query(..., description="New task status")
) -> Task:
    """Update only the status of a task"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    task = tasks_db[task_id]
    task.status = new_status
    task.updated_at = datetime.utcnow()
    tasks_db[task_id] = task
    return task

@app.delete(
    "/api/v1/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task"
)
async def delete_task(task_id: int = Path(..., gt=0, description="Task ID")):
    """Delete a task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    del tasks_db[task_id]
    return None

# User endpoints
@app.post(
    "/api/v1/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create a new user"
)
async def create_user(user_data: UserCreate) -> User:
    """Create a new user"""
    # Check if username or email already exists
    for user in users_db.values():
        if user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    user_id = get_next_user_id()
    user = User(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        is_active=True,
        created_at=datetime.utcnow()
    )
    users_db[user_id] = user
    return user

@app.get(
    "/api/v1/users",
    response_model=List[User],
    tags=["Users"],
    summary="Get all users"
)
async def get_users(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
) -> List[User]:
    """Get all users with optional filtering and pagination"""
    users = list(users_db.values())
    
    # Apply filters
    if is_active is not None:
        users = [u for u in users if u.is_active == is_active]
    
    # Apply pagination
    return users[skip:skip + limit]

@app.get(
    "/api/v1/users/{user_id}",
    response_model=User,
    tags=["Users"],
    summary="Get a specific user"
)
async def get_user(user_id: int = Path(..., gt=0, description="User ID")) -> User:
    """Get a user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return users_db[user_id]

@app.delete(
    "/api/v1/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Delete a user"
)
async def delete_user(user_id: int = Path(..., gt=0, description="User ID")):
    """Delete a user by ID (soft delete - marks as inactive)"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    users_db[user_id].is_active = False
    return None

# Statistics endpoints
@app.get(
    "/api/v1/stats/tasks",
    tags=["Statistics"],
    summary="Get task statistics"
)
async def get_task_stats() -> Dict[str, Any]:
    """Get task statistics"""
    total_tasks = len(tasks_db)
    
    if total_tasks == 0:
        return {
            "total": 0,
            "by_status": {},
            "by_priority": {}
        }
    
    stats_by_status = {}
    stats_by_priority = {}
    
    for task in tasks_db.values():
        # Count by status
        status_key = task.status.value
        stats_by_status[status_key] = stats_by_status.get(status_key, 0) + 1
        
        # Count by priority
        priority_key = task.priority.value
        stats_by_priority[priority_key] = stats_by_priority.get(priority_key, 0) + 1
    
    return {
        "total": total_tasks,
        "by_status": stats_by_status,
        "by_priority": stats_by_priority
    }

@app.get(
    "/api/v1/stats/users",
    tags=["Statistics"],
    summary="Get user statistics"
)
async def get_user_stats() -> Dict[str, Any]:
    """Get user statistics"""
    total_users = len(users_db)
    active_users = sum(1 for user in users_db.values() if user.is_active)
    inactive_users = total_users - active_users
    
    return {
        "total": total_users,
        "active": active_users,
        "inactive": inactive_users
    }

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

# Application startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("🚀 Application starting up...")
    print("📚 API documentation available at: /docs")
    print("📖 Alternative documentation at: /redoc")

@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("👋 Application shutting down...")

# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
