from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import NamedTuple
from miningsimulation.station import UnloadStation
from miningsimulation.truck import Truck

DEFAULT_TRANSIT_TIME_MINUTES = 30
DEFAULT_UNLOAD_TIME_MINUTES = 5


class StateManager(ABC):
    @abstractmethod
    def onboard_trucks(self, timestamp: int, trucks: list[Truck]) -> None:
        pass

    @abstractmethod
    def remove_trucks(self, timstamp: int) -> list[Truck]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class MiningSitesManager(StateManager):
    # TODO maybe actually have mining site objects

    def __init__(self):
        # store trucks under {expiration_timestamp: list[Truck]}
        self.trucks = defaultdict(list)

    def onboard_trucks(self, timestamp: int, trucks: list[Truck]) -> None:
        for truck in trucks:
            time_truck_will_leave = timestamp + truck.mining_session_duration_minutes()
            self.trucks[time_truck_will_leave].append(truck)

    def remove_trucks(self, timestamp: int) -> list[Truck]:
        if timestamp not in self.trucks:
            return []
        return self.trucks.pop(timestamp)
    
    def __str__(self) -> str:
        s = ""
        for departure_time, truck_list in self.trucks.items():
            for truck in truck_list:
                s += f"{truck} leaving at {departure_time}, "
        return f"MiningSitesManager\n\t\ttrucks: " + s


class RouteManager(StateManager):
    def __init__(self, id: str, transit_time_minutes: int=DEFAULT_TRANSIT_TIME_MINUTES):
        self.id = id
        self.truck_queue = deque()
        self.transit_time_minutes = transit_time_minutes

    def onboard_trucks(self, timestamp: int, trucks: list[Truck]) -> None:
        if len(trucks) == 0:
            return
        # store the trucks with the future timestamp that they should be released at
        self.truck_queue.append((timestamp + self.transit_time_minutes, trucks))

    def remove_trucks(self, timestamp: int) -> list[Truck]:
        if len(self.truck_queue) == 0:
            return []
        expir_timestamp, trucks = self.truck_queue[0]
        if expir_timestamp == timestamp:
            self.truck_queue.popleft()
            return trucks
        return []
    
    def __str__(self):
        s = ""
        for exp_timestamp, trucks in self.truck_queue:
            s += f"\n\t\tdeparting at {exp_timestamp}: "
            for truck in trucks:
                s += f"{truck}, "
        return f"RouteManager ({self.id})\n\t\ttrucks:" + s


class StationsManager(StateManager):
    def __init__(self, num_unload_stations: int, unload_time_minutes: int=DEFAULT_UNLOAD_TIME_MINUTES):
        self.unload_stations = []
        for i in range(num_unload_stations):
            self.unload_stations.append(UnloadStation(f"unload_station_{i}"))
        self.unload_time_minutes = unload_time_minutes

    def onboard_trucks(self, timestamp: int, trucks: list[Truck]) -> None:
        """
        Send each truck to the next station that has the smallest queue
        """
        # TODO - introduce a smarter add & remove to make this more efficient
        for truck in trucks:
            next_station_i = self.unload_stations.index(min(self.unload_stations))
            self.unload_stations[next_station_i].enqueue((timestamp + self.unload_time_minutes, truck))

    def remove_trucks(self, timestamp: int) -> list[Truck]:
        trucks = []
        for unload_station in self.unload_stations:
            if len(unload_station) > 0 and unload_station.next_departure_time() == timestamp:
                _, truck = unload_station.dequeue()
                trucks.append(truck)
        return trucks
    
    def __str__(self):
        s = f"StationsManager\n\t\tunload stations:"
        for station in self.unload_stations:
            s += f"\n{station}"
        return s


class Managers(NamedTuple):
    mining_sites: MiningSitesManager
    sites_to_stations: RouteManager
    stations: StationsManager
    stations_to_sites: RouteManager