
from pydantic import BaseModel
from typing import List, Optional

class PreferencesModel(BaseModel):
    city: str
    interests: List[str]
    start_time: str
    end_time: str
    budget: int
    starting_point: Optional[str] = None

class PreferencesPayload(BaseModel):
    user_id: str
    preferences: PreferencesModel

# New model for itinerary request
class ItineraryRequest(BaseModel):
    user_id: str
    city: str
    interests: List[str]
    start_time: str
    end_time: str
    budget: int
