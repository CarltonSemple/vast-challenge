from time import sleep
from miningsimulation.logging import Logger
from miningsimulation.managers import (
    Managers,
    MiningSitesManager,
    RouteManager,
    StationsManager,
)
from miningsimulation.station import UnloadStation
from miningsimulation.truck import Truck


class Simulation:
    def __init__(
            self,
            run_duration_minutes: int,
            num_mining_trucks: int,
            num_unload_stations: int,
            tick_interval_minutes: int=1,
            sleep_seconds_between_ticks: int=0):
        self.tick_interval = tick_interval_minutes
        self.run_duration = run_duration_minutes
        self.current_tick = 0
        self.start_timestamp = 0
        self.num_mining_trucks = num_mining_trucks
        self.num_unload_stations = num_unload_stations
        self.sleep_seconds_between_ticks = sleep_seconds_between_ticks

    def _generate_trucks_stations_managers(self) -> None:        
        self.managers = Managers(
            mining_sites=MiningSitesManager(),
            sites_to_stations=RouteManager("RouteSitesToStations"),
            stations=StationsManager(self.num_unload_stations),
            stations_to_sites=RouteManager("RouteStationsToSites"),
        )

        # Place the trucks at mining sites to begin
        trucks = []
        for i in range(self.num_mining_trucks):
            trucks.append(Truck(f"truck_{i}"))
        self.managers.mining_sites.onboard_trucks(self.start_timestamp, trucks)

    def run_to_completion(self) -> None:
        logger = Logger()
        logger.run_logging_thread()

        self._generate_trucks_stations_managers()

        while (self.current_tick + self.start_timestamp < self.run_duration + self.start_timestamp):
            print(f"minute: {self.current_tick + self.start_timestamp}")
            self.run_tick(self.current_tick + self.start_timestamp)
            self.current_tick += self.tick_interval

        Logger.log_queue.put(None)
    
    def run_tick(self, timestamp: int) -> None:
        # unload stations queue -> route to mining sites
        # (clearing station queues before trying to add new trucks)
        self.managers.stations_to_sites.onboard_trucks(
            timestamp, self.managers.stations.remove_trucks(timestamp))
        # route to mining sites -> mining sites
        self.managers.mining_sites.onboard_trucks(
            timestamp, self.managers.stations_to_sites.remove_trucks(timestamp))
        # mining site -> route to stations
        self.managers.sites_to_stations.onboard_trucks(
            timestamp, self.managers.mining_sites.remove_trucks(timestamp))
        # route to stations -> stations queue
        self.managers.stations.onboard_trucks(
            timestamp, self.managers.sites_to_stations.remove_trucks(timestamp))
        
        self.print_state()
        
        if self.sleep_seconds_between_ticks > 0:
            sleep(self.sleep_seconds_between_ticks)

    def print_state(self) -> None:
        print("---------------------------------------------------------")
        for manager in self.managers:
            print(manager)
