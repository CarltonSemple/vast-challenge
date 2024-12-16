import csv
import os
from queue import Queue
import threading


class Logger:
    log_queue = Queue(-1)
    logging_thread = None

    def __init__(self):
        pass

    def run_logging_thread(self) -> None:
        Logger.logging_thread = threading.Thread(target=write_to_log_files)
        Logger.logging_thread.start()


def write_to_log_files() -> None:
    while True:
        val = Logger.log_queue.get()
        if val is None:
            break
        log_type, log_content = val

        if log_type == "mining_session":
            write_mining_session(log_content)
        elif log_type == "station_size":
            write_station_size(log_content)


def write_mining_session(log_content: dict[str, any]) -> None:
    if not os.path.exists("mining_sessions.csv"):
        # write the header
        with open("mining_sessions.csv", "w") as f:
            w = csv.writer(f)
            w.writerow(log_content.keys())

    with open("mining_sessions.csv", "a") as f:
        w = csv.writer(f)
        w.writerow(log_content.values())


def write_station_size(log_content: dict[str, any]) -> None:
    if not os.path.exists("station_sizes.csv"):
        # write the header
        with open("station_sizes.csv", "w") as f:
            w = csv.writer(f)
            w.writerow(log_content.keys())

    with open("station_sizes.csv", "a") as f:
        w = csv.writer(f)
        w.writerow(log_content.values())


def log_mining_session(truck_id: str, timestamp: int, duration_minutes: int) -> None:
    Logger.log_queue.put(("mining_session", {
        "timestamp": timestamp,
        "truck_id": truck_id,
        "duration_minutes": duration_minutes,
    }))


def log_station_size(timestamp: int, station_id: str, station_size: int) -> None:
    Logger.log_queue.put(("station_size", {
        "timestamp": timestamp,
        "station_id": station_id,
        "station_size": station_size,
    }))
