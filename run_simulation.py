import os
from miningsimulation.simulation import Simulation

def main() -> None:
    data_files = ["mining_sessions.csv", "station_sizes.csv"]
    for file in data_files:
        if os.path.exists(file):
            os.remove(file)

    sim = Simulation(
        run_duration_minutes=72 * 60,
        num_mining_trucks=10,
        num_unload_stations=8,
        tick_interval_minutes=1,
        sleep_seconds_between_ticks=0,
    )

    sim.run_to_completion()

if __name__ == "__main__":
    main()
