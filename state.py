# creating a shared state 

from typing import TypedDict, Optional

class WeatherState(TypedDict):
    question: str
    route: Optional[str]
    city: Optional[str]
    answer: Optional[str]