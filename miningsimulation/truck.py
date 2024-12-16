import random
from miningsimulation.logging import log_mining_session

class Truck:
    def __init__(self, id: str):
        self.id: int = id

    def mining_session_duration_minutes(self, timestamp: int) -> int:
        duration = random.randint(60, 5 * 60)
        log_mining_session(self.id, timestamp, duration)
        return duration
    
    def __str__(self) -> str:
        return f"{self.id}"
