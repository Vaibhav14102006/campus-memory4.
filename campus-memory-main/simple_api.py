"""
Simple Mock API Server for Event Management with AI Features
Runs on port 8001 without heavy dependencies
Includes mock AI poster analysis endpoints
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import uvicorn
import json

app = FastAPI(title="Event Management API - Enhanced Mock")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
events_db = [
    {
        "eventId": "evt1",
        "title": "Tech Fest 2026",
        "category": "Technical",
        "date": "2026-03-15",
        "time": "10:00 AM",
        "location": "Main Auditorium",
        "school": "Engineering",
        "posterUrl": "https://via.placeholder.com/300"
    },
    {
        "eventId": "evt2",
        "title": "Cultural Night",
        "category": "Cultural",
        "date": "2026-03-20",
        "time": "6:00 PM",
        "location": "Open Ground",
        "school": "Arts",
        "posterUrl": "https://via.placeholder.com/300"
    }
]

attendance_db = []
users_db = {}

@app.get("/")
async def root():
    return {"message": "Event Management API - Mock Server", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Event endpoints
@app.get("/events")
async def get_events():
    return events_db

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    for event in events_db:
        if event["eventId"] == event_id:
            return event
    return {"error": "Event not found"}, 404

@app.post("/events")
async def create_event(event: dict):
    event["eventId"] = f"evt{len(events_db) + 1}"
    events_db.append(event)
    return event

@app.put("/events/{event_id}")
async def update_event(event_id: str, event: dict):
    for i, e in enumerate(events_db):
        if e["eventId"] == event_id:
            events_db[i] = {**e, **event}
            return events_db[i]
    return {"error": "Event not found"}, 404

@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    global events_db
    events_db = [e for e in events_db if e["eventId"] != event_id]
    return {"message": "Event deleted"}

# Attendance endpoints
@app.get("/attendance")
async def get_attendance():
    return attendance_db

@app.post("/attendance")
async def mark_attendance(attendance: dict):
    attendance["id"] = f"att{len(attendance_db) + 1}"
    attendance_db.append(attendance)
    return attendance

# Dashboard endpoints
@app.get("/dashboard/{role}/{user_id}")
async def get_dashboard(role: str, user_id: str):
    if role == "student":
        # Return student-specific dashboard data
        return {
            "studentId": user_id,
            "totalEventsAttended": 5,
            "presentCount": 4,
            "odGrantedCount": 1,
            "attendedEvents": [
                {
                    "eventId": "evt1",
                    "title": "Tech Fest 2026",
                    "date": "2026-03-15",
                    "category": "Technical",
                    "odGranted": False
                },
                {
                    "eventId": "evt2",
                    "title": "Cultural Night",
                    "date": "2026-03-20",
                    "category": "Cultural",
                    "odGranted": True
                },
                {
                    "eventId": "evt3",
                    "title": "Sports Day",
                    "date": "2026-03-10",
                    "category": "Sports",
                    "odGranted": False
                },
                {
                    "eventId": "evt4",
                    "title": "Workshop: AI & ML",
                    "date": "2026-03-05",
                    "category": "Workshop",
                    "odGranted": False
                },
                {
                    "eventId": "evt5",
                    "title": "Annual Day",
                    "date": "2026-02-28",
                    "category": "Cultural",
                    "odGranted": False
                }
            ]
        }
    elif role == "teacher":
        # Return teacher-specific dashboard data
        return {
            "teacherId": user_id,
            "school": "Engineering",
            "schoolEvents": events_db,
            "totalStudents": 150,
            "averageAttendance": 85.5
        }
    elif role == "coordinator":
        # Return coordinator dashboard data
        return {
            "coordinatorId": user_id,
            "totalEvents": len(events_db),
            "upcomingEvents": len([e for e in events_db if e["date"] >= "2026-03-15"]),
            "totalAttendance": len(attendance_db),
            "events": events_db
        }
    else:
        # Default response
        return {
            "role": role,
            "userId": user_id,
            "events": events_db,
            "stats": {
                "totalEvents": len(events_db),
                "totalAttendance": len(attendance_db),
                "activeUsers": len(users_db)
            }
        }

# AI Poster Analysis endpoints (Mock)
@app.post("/analyze/poster")
async def analyze_poster(file: UploadFile = File(...)):
    """Mock AI poster analysis"""
    # Return mock analysis result
    return {
        "success": True,
        "extractedData": {
            "title": "Sample Event from Poster",
            "category": "Technical",
            "school": "Amity School of Engineering & Technology",
            "date": "2026-03-25",
            "time": "2:00 PM",
            "location": "Auditorium Hall A",
            "description": "Extracted from poster using AI"
        },
        "confidence": {
            "category": 0.92,
            "school": 0.88,
            "overall": 0.85
        },
        "rawText": "TECH FEST 2026\nAmity School of Engineering\nDate: March 25, 2026",
        "needsReview": True,
        "message": "Analysis complete. Please review and edit the extracted data before saving."
    }

@app.post("/events/from-poster")
async def create_event_from_poster(
    file: UploadFile = File(...),
    coordinatorId: str = Form(...)
):
    """Create event from poster analysis (Mock)"""
    # Simulate poster analysis and event creation
    new_event = {
        "eventId": f"evt{len(events_db) + 1}",
        "title": "AI Extracted Event",
        "category": "Technical",
        "date": "2026-03-25",
        "time": "2:00 PM",
        "location": "Auditorium Hall A",
        "school": "Amity School of Engineering & Technology",
        "posterUrl": "https://via.placeholder.com/300",
        "createdBy": coordinatorId,
        "createdAt": datetime.now().isoformat(),
        "source": "ai_poster_analysis"
    }
    events_db.append(new_event)
    
    return {
        "success": True,
        "event": new_event,
        "message": "Event created from poster. Please review and edit if needed."
    }

# Sub-user management endpoints (Mock)
@app.get("/subusers")
async def get_subusers():
    """Get all sub-users"""
    return []

@app.post("/subusers")
async def create_subuser(subuser: dict):
    """Create a new sub-user"""
    return {"success": True, "subuser": subuser}

# OD management endpoints
@app.patch("/attendance/{attendance_id}/od")
async def grant_od(attendance_id: str, data: dict):
    """Grant OD to a student"""
    return {
        "success": True,
        "message": "OD granted successfully",
        "attendanceId": attendance_id
    }

# Reporting endpoints
@app.post("/reports/export")
async def export_report(filters: dict):
    """Export report"""
    return {
        "success": True,
        "message": "Report exported",
        "downloadUrl": "http://localhost:8001/downloads/report.csv"
    }

if __name__ == "__main__":
    print("🚀 Starting Enhanced Mock Event Management API Server...")
    print("📍 Server running at: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("\n✨ Features:")
    print("   ✅ Event Management (CRUD)")
    print("   ✅ Attendance Tracking")
    print("   ✅ Dashboard APIs (Student/Teacher/Coordinator)")
    print("   ✅ AI Poster Analysis (Mock)")
    print("   ✅ Sub-user Management (Mock)")
    print("   ✅ OD Management (Mock)")
    print("   ✅ Report Export (Mock)")
    uvicorn.run(app, host="0.0.0.0", port=8001)
