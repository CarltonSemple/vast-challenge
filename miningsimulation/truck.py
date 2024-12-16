import random

class Truck:
    def __init__(self, id: str):
        self.id: int = id

    def mining_session_duration_minutes(self) -> int:
        return random.randint(60, 5 * 60)
    
    def __str__(self) -> str:
        return f"{self.id}"
