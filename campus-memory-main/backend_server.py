"""
Campus Memory + ML Integration Backend
FastAPI server that combines the ML models with the Campus Memory platform
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

# Import ML systems
from recommendation_system import EventRecommendationSystem
from event_guidance_system import EventGuidanceSystem

app = FastAPI(
    title="Campus Memory ML API",
    description="Integrated ML-powered event recommendations and campus memory system",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML systems
try:
    recommender = EventRecommendationSystem()
    guidance_system = EventGuidanceSystem()
    print("✅ ML Models loaded successfully!")
except Exception as e:
    print(f"⚠️  Warning: Could not load ML models: {e}")
    recommender = None
    guidance_system = None

# Pydantic models for request/response
class StudentProfile(BaseModel):
    branch: str
    year: int
    gender: str
    skill_level: str
    age: Optional[int] = None
    previous_participation: Optional[str] = "Low"
    team_size: Optional[int] = 3
    participated_alone: Optional[int] = 0
    achievement: Optional[str] = "Participation"

class EventInfo(BaseModel):
    name: str
    type: str
    level: str
    duration_days: int
    description: Optional[str] = ""
    date: Optional[str] = ""

class Problem(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    category: str
    severity: str
    status: str
    reportedBy: str
    reportedDate: Optional[str] = None
    upvotes: Optional[int] = 0
    college: str
    anonymous: Optional[bool] = False

class WisdomTip(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    category: str
    author: str
    college: str
    date: Optional[str] = None
    upvotes: Optional[int] = 0
    helpful: Optional[int] = 0

class Alert(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    severity: str
    category: str
    predictedDate: str
    college: str
    createdBy: str
    confidence: Optional[float] = 0.85

# In-memory storage (replace with database in production)
DATA_DIR = "campus_data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename, default=None):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default if default is not None else []

def save_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== Health Check ====================
@app.get("/")
def root():
    return {
        "service": "Campus Memory ML API",
        "status": "running",
        "ml_models": {
            "recommender": recommender is not None,
            "guidance_system": guidance_system is not None
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": recommender is not None and guidance_system is not None
    }

# ==================== ML Endpoints ====================
@app.post("/api/ml/recommend-events")
def recommend_events(student: StudentProfile, top_n: int = 5):
    """Get personalized event recommendations for a student"""
    if recommender is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    try:
        # Default event list
        event_list = [
            {'name': 'Hacksetu', 'type': 'Hackathon', 'level': 'National', 'duration_days': 2},
            {'name': 'Anveshan', 'type': 'Hackathon', 'level': 'University', 'duration_days': 1},
            {'name': 'Ami Chroma', 'type': 'Cultural', 'level': 'University', 'duration_days': 3},
            {'name': 'Smart India Hackathon', 'type': 'Hackathon', 'level': 'National', 'duration_days': 3},
            {'name': 'Init Maths', 'type': 'Training', 'level': 'Department', 'duration_days': 6},
            {'name': 'Convocation', 'type': 'Ceremony', 'level': 'University', 'duration_days': 1},
            {'name': 'TechFest', 'type': 'Technical', 'level': 'University', 'duration_days': 2},
            {'name': 'Code Sprint', 'type': 'Hackathon', 'level': 'Department', 'duration_days': 1},
        ]
        
        student_dict = student.dict()
        recommendations = recommender.recommend_events_for_student(
            student_dict, 
            event_list, 
            top_n=top_n
        )
        
        return {
            "status": "success",
            "student_profile": student_dict,
            "recommendations": recommendations,
            "total_events": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/api/ml/event-guidance")
def event_guidance(student: StudentProfile, event_name: str):
    """Get comprehensive guidance for an event registration"""
    if guidance_system is None:
        raise HTTPException(status_code=503, detail="Guidance system not available")
    
    try:
        student_dict = student.dict()
        guidance = guidance_system.get_recommendations_for_registered_event(
            student_dict, 
            event_name
        )
        
        return {
            "status": "success",
            "event_name": event_name,
            "guidance": guidance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating guidance: {str(e)}")

@app.post("/api/ml/predict-event-outcome")
def predict_event_outcome(student: StudentProfile, event: EventInfo):
    """Predict likely satisfaction and recommendation for a specific event"""
    if recommender is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    try:
        student_dict = student.dict()
        event_dict = event.dict()
        
        prediction = recommender.predict_for_event(student_dict, event_dict)
        
        return {
            "status": "success",
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting outcome: {str(e)}")

# ==================== Campus Data Endpoints ====================
@app.get("/api/colleges/{college_id}/problems")
def get_problems(college_id: str, category: Optional[str] = None):
    """Get all problems for a college"""
    problems = load_json(f"problems_{college_id}.json", [])
    
    if category and category != "all":
        problems = [p for p in problems if p.get("category") == category]
    
    return {"status": "success", "problems": problems, "total": len(problems)}

@app.post("/api/colleges/{college_id}/problems")
def create_problem(college_id: str, problem: Problem):
    """Report a new problem"""
    problems = load_json(f"problems_{college_id}.json", [])
    
    problem_data = problem.dict()
    problem_data["id"] = f"p{int(datetime.now().timestamp() * 1000)}"
    problem_data["reportedDate"] = datetime.now().strftime("%Y-%m-%d")
    problem_data["college"] = college_id
    
    problems.append(problem_data)
    save_json(f"problems_{college_id}.json", problems)
    
    return {"status": "success", "problem": problem_data}

@app.put("/api/colleges/{college_id}/problems/{problem_id}")
def update_problem(college_id: str, problem_id: str, problem: Problem):
    """Update a problem"""
    problems = load_json(f"problems_{college_id}.json", [])
    
    for i, p in enumerate(problems):
        if p["id"] == problem_id:
            problem_data = problem.dict()
            problem_data["id"] = problem_id
            problems[i] = problem_data
            save_json(f"problems_{college_id}.json", problems)
            return {"status": "success", "problem": problem_data}
    
    raise HTTPException(status_code=404, detail="Problem not found")

@app.delete("/api/colleges/{college_id}/problems/{problem_id}")
def delete_problem(college_id: str, problem_id: str):
    """Delete a problem"""
    problems = load_json(f"problems_{college_id}.json", [])
    problems = [p for p in problems if p["id"] != problem_id]
    save_json(f"problems_{college_id}.json", problems)
    return {"status": "success", "message": "Problem deleted"}

@app.get("/api/colleges/{college_id}/wisdom")
def get_wisdom(college_id: str, category: Optional[str] = None):
    """Get wisdom tips for a college"""
    wisdom = load_json(f"wisdom_{college_id}.json", [])
    
    if category and category != "all":
        wisdom = [w for w in wisdom if w.get("category") == category]
    
    return {"status": "success", "wisdom": wisdom, "total": len(wisdom)}

@app.post("/api/colleges/{college_id}/wisdom")
def create_wisdom(college_id: str, wisdom: WisdomTip):
    """Share a wisdom tip"""
    wisdom_list = load_json(f"wisdom_{college_id}.json", [])
    
    wisdom_data = wisdom.dict()
    wisdom_data["id"] = f"w{int(datetime.now().timestamp() * 1000)}"
    wisdom_data["date"] = datetime.now().strftime("%Y-%m-%d")
    wisdom_data["college"] = college_id
    
    wisdom_list.append(wisdom_data)
    save_json(f"wisdom_{college_id}.json", wisdom_list)
    
    return {"status": "success", "wisdom": wisdom_data}

@app.get("/api/colleges/{college_id}/alerts")
def get_alerts(college_id: str):
    """Get alerts for a college"""
    alerts = load_json(f"alerts_{college_id}.json", [])
    return {"status": "success", "alerts": alerts, "total": len(alerts)}

@app.post("/api/colleges/{college_id}/alerts")
def create_alert(college_id: str, alert: Alert):
    """Create a new alert"""
    alerts = load_json(f"alerts_{college_id}.json", [])
    
    alert_data = alert.dict()
    alert_data["id"] = f"a{int(datetime.now().timestamp() * 1000)}"
    alert_data["college"] = college_id
    
    alerts.append(alert_data)
    save_json(f"alerts_{college_id}.json", alerts)
    
    return {"status": "success", "alert": alert_data}

# ==================== Analytics Endpoints ====================
@app.get("/api/colleges/{college_id}/analytics")
def get_analytics(college_id: str):
    """Get analytics for a college"""
    problems = load_json(f"problems_{college_id}.json", [])
    wisdom = load_json(f"wisdom_{college_id}.json", [])
    alerts = load_json(f"alerts_{college_id}.json", [])
    
    # Problem analytics
    problem_categories = {}
    problem_status = {}
    for p in problems:
        cat = p.get("category", "Unknown")
        status = p.get("status", "Unknown")
        problem_categories[cat] = problem_categories.get(cat, 0) + 1
        problem_status[status] = problem_status.get(status, 0) + 1
    
    # Wisdom analytics
    wisdom_categories = {}
    for w in wisdom:
        cat = w.get("category", "Unknown")
        wisdom_categories[cat] = wisdom_categories.get(cat, 0) + 1
    
    return {
        "status": "success",
        "analytics": {
            "total_problems": len(problems),
            "total_wisdom": len(wisdom),
            "total_alerts": len(alerts),
            "problem_by_category": problem_categories,
            "problem_by_status": problem_status,
            "wisdom_by_category": wisdom_categories
        }
    }

# ==================== Events Management ====================
@app.get("/api/events")
def get_all_events():
    """Get all available events"""
    events = load_json("events.json", [
        {
            "id": "evt1",
            "name": "Hacksetu",
            "type": "Hackathon",
            "level": "National",
            "duration_days": 2,
            "description": "National level hackathon focused on innovative solutions",
            "date": "2026-03-15",
            "location": "Main Campus",
            "registrations": 0,
            "max_participants": 500
        },
        {
            "id": "evt2",
            "name": "Smart India Hackathon",
            "type": "Hackathon",
            "level": "National",
            "duration_days": 3,
            "description": "Government initiative for solving real-world problems",
            "date": "2026-04-20",
            "location": "Multiple Locations",
            "registrations": 0,
            "max_participants": 1000
        },
        {
            "id": "evt3",
            "name": "Ami Chroma",
            "type": "Cultural",
            "level": "University",
            "duration_days": 3,
            "description": "Annual cultural fest with competitions and performances",
            "date": "2026-03-25",
            "location": "Auditorium",
            "registrations": 0,
            "max_participants": 2000
        },
        {
            "id": "evt4",
            "name": "Init Maths",
            "type": "Training",
            "level": "Department",
            "duration_days": 6,
            "description": "Mathematics workshop for competitive programming",
            "date": "2026-03-10",
            "location": "Department Block",
            "registrations": 0,
            "max_participants": 100
        },
        {
            "id": "evt5",
            "name": "TechFest",
            "type": "Technical",
            "level": "University",
            "duration_days": 2,
            "description": "Technical festival with coding, robotics, and AI competitions",
            "date": "2026-04-05",
            "location": "Tech Park",
            "registrations": 0,
            "max_participants": 800
        },
    ])
    
    return {"status": "success", "events": events, "total": len(events)}

@app.post("/api/events/{event_id}/register")
def register_for_event(event_id: str, student: StudentProfile):
    """Register a student for an event and get ML-powered guidance"""
    events = load_json("events.json", [])
    event = next((e for e in events if e["id"] == event_id), None)
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get ML guidance if available
    guidance = None
    if guidance_system:
        try:
            guidance = guidance_system.get_recommendations_for_registered_event(
                student.dict(),
                event["name"]
            )
        except Exception as e:
            print(f"Warning: Could not generate guidance: {e}")
    
    # Update event registrations
    event["registrations"] = event.get("registrations", 0) + 1
    save_json("events.json", events)
    
    return {
        "status": "success",
        "message": f"Successfully registered for {event['name']}",
        "event": event,
        "guidance": guidance
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("🚀 Starting Campus Memory ML Backend Server")
    print("="*80)
    print("📡 API will be available at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
