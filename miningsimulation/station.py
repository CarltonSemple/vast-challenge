from collections import deque


class UnloadStation:
    def __init__(self, id: str):
        self.id: int = id
        self.truck_queue = deque()

    def next_departure_time(self) -> int:
        if len(self.truck_queue) <= 0:
            raise RuntimeError("called next_departure_time with no trucks in queue")
        timestamp, _ = self.truck_queue[0]
        return timestamp

    def enqueue(self, timestamp_and_truck: tuple) -> None:
        self.truck_queue.append(timestamp_and_truck)

    def dequeue(self) -> tuple:
        if len(self.truck_queue) <= 0:
            raise RuntimeError("called dequeue with no trucks in queue")
        return self.truck_queue.popleft()

    def __lt__(self, other):
        return len(self.truck_queue) < len(other.truck_queue)
    
    def __len__(self):
        return len(self.truck_queue)
    
    def __str__(self):
        s = ""
        for timestamp, truck in self.truck_queue:
            s += f"{truck} leaving at {timestamp}, "
        return f"\t\t\t{self.id}\n\t\t\t\t" + s
