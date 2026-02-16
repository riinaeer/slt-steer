from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


"""
Enums

Some not yet implemented because of tests
"""
class AlcoholUse(str, Enum):
    NONE = "none"
    RARE = "rare"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    
class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    VIGOROUS = "vigorous"

class UserRole(str, Enum):
    PATIENT = "patient"
    PROFESSIONAL = "professional"

class SenderType(str, Enum):
    USER = "user"
    BOT = "bot"
    PROFESSIONAL = "professional"

class Classification(str, Enum):
    SAFE = "safe"
    NEEDS_REVIEW = "needs_review"
    EMERGENCY = "emergency"

class ChatStatus(str, Enum):
    OPEN = "open"
    WAITING = "waiting_for_professional"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


"""
Base models
"""
class BloodPressure(BaseModel):
    systolic: int = Field(..., ge=50, le=300, description="mmHg")
    diastolic: int = Field(..., ge=30, le=200, description="mmHg")

class PatientInfo(BaseModel):
    weight: float
    height: float
    age: int
    conditions: List[str] = []
    avg_blood_pressure: BloodPressure
    risk_factors: List[str] = []
    alcohol_use: AlcoholUse
    allergies: List[str] = []
    activity: ActivityLevel
    medications: List[str] = []
    heart_procedures: List[str] = []

class UserModel(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.PATIENT
    patient_info: Optional[PatientInfo] = None

class ChatModel(BaseModel):
    user_id: str
    status: str
    assigned_professional_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class MessageModel(BaseModel):
    chat_id: str
    sender: SenderType
    content: str
    classification: Classification = Classification.SAFE
    flagged_for_human: bool = False
    created_at: datetime
    updated_at: datetime