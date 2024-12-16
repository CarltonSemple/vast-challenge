from miningsimulation.simulation import Simulation

def main() -> None:
    sim = Simulation(
        run_duration_minutes=30,
        num_mining_trucks=1,
        num_unload_stations=1,
        tick_interval=1,
        sleep_seconds_between_ticks=3,
    )

    sim.run_to_completion()

if __name__ == "__main__":
    main()
