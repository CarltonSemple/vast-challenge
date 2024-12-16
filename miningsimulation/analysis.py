

from collections import defaultdict
import csv


MINING_SESSIONS_FILEPATH = "./mining_sessions.csv"
STATION_SIZES_FILEPATH = "./station_sizes.csv"


def get_truck_mining_session_info(mining_sessions_filepath: str=MINING_SESSIONS_FILEPATH) -> dict[str,any]:
    truck_mining_sessions = defaultdict(list)

    with open(mining_sessions_filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            truck_id = row["truck_id"]
            truck_mining_sessions[truck_id].append({
                'timestamp': int(row["timestamp"]),
                'duration': int(row["duration_minutes"]),
            })

    return truck_mining_sessions


def get_station_info(station_sizes_filepath: str=STATION_SIZES_FILEPATH) -> dict[str,any]:
    station_sizes = defaultdict(list)

    with open(station_sizes_filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            station_id = row["station_id"]
            station_sizes[station_id].append({
                'timestamp': int(row["timestamp"]),
                'size': int(row["station_size"]),
            })

    return station_sizes


def print_mining_session_insights(truck_mining_sessions: dict[str,any]) -> None:
    print("MINING SESSIONS\nNumber of Mining Sessions")
    for truck in truck_mining_sessions:
        print(f"{truck}: {len(truck_mining_sessions[truck])}")
    print('\n')

    print("Truck with the longest session")
    max_session_duration_truck = ''
    max_session_duration = 0
    for truck in truck_mining_sessions:
        for session_info in truck_mining_sessions[truck]:
            if session_info['duration'] > max_session_duration:
                max_session_duration = session_info['duration']
                max_session_duration_truck = truck
    print(f"{max_session_duration_truck} with a session duration of {max_session_duration} minutes.\n")


def print_station_info(station_sizes: dict[str,any]) -> None:
    print("STATION INFO")

    for station in station_sizes:
        minutes_occupied = 0
        for minute in station_sizes[station]:
            if minute["size"] > 0:
                minutes_occupied += 1
        print(f"{station} spent {minutes_occupied} minutes occupied")


def analyze_results() -> None:
    truck_mining_sessions = get_truck_mining_session_info()
    print_mining_session_insights(truck_mining_sessions)

    station_sizes = get_station_info()
    print_station_info(station_sizes)
