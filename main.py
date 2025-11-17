import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import create_document

app = FastAPI(title="Locat8 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WaitlistIn(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    source: Optional[str] = None

class AnalyticsIn(BaseModel):
    type: str
    email: Optional[EmailStr] = None
    page: Optional[str] = None
    source: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Locat8 Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.post("/api/waitlist")
async def join_waitlist(payload: WaitlistIn, request: Request):
    try:
        referrer = request.headers.get("referer")
        user_agent = request.headers.get("user-agent")
        data = {
            "email": payload.email,
            "name": payload.name,
            "source": payload.source,
            "referrer": referrer,
            "user_agent": user_agent,
        }
        doc_id = create_document("waitlist", data)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analytics")
async def analytics_event(payload: AnalyticsIn, request: Request):
    try:
        referrer = request.headers.get("referer")
        user_agent = request.headers.get("user-agent")
        data = {
            "type": payload.type,
            "email": payload.email,
            "page": payload.page,
            "source": payload.source,
            "referrer": referrer,
            "user_agent": user_agent,
        }
        doc_id = create_document("analytics", data)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
