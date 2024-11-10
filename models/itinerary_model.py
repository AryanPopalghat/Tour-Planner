from pydantic import BaseModel
from typing import List

class ItineraryItem(BaseModel):
    name: str
    time: str
    entry_fee: str
    transportation: str = "Walk"  # Default transportation method

class Itinerary(BaseModel):
    items: List[ItineraryItem]

    def add_item(self, name: str, time: str, entry_fee: str, transportation: str = "Walk"):
        self.items.append(ItineraryItem(name=name, time=time, entry_fee=entry_fee, transportation=transportation))

    def generate_summary(self):
        return [{"name": item.name, "time": item.time, "entry_fee": item.entry_fee, "transportation": item.transportation} for item in self.items]
