"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Waitlist(BaseModel):
    """
    Waitlist collection schema for Locat8
    Collection name: "waitlist"
    """
    email: EmailStr = Field(..., description="User email for the waitlist")
    name: Optional[str] = Field(None, description="Optional name")
    source: Optional[str] = Field(None, description="Traffic source or UTM source")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    user_agent: Optional[str] = Field(None, description="User agent string from the browser")

class Analytics(BaseModel):
    """Generic analytics events collection
    Collection name: "analytics"
    """
    type: Literal["signup", "cta_click", "view"] = Field(..., description="Event type")
    email: Optional[EmailStr] = Field(None, description="Associated email if available")
    page: Optional[str] = Field(None, description="Page path")
    source: Optional[str] = Field(None, description="UTM or source tag")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    user_agent: Optional[str] = Field(None, description="User agent string")
