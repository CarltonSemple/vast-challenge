# Vast Challenge - Carlton Semple

Notes:
waiting at mining sites is truck-dependent. unlimited mining sites.  
mining unload stations have 1 truck at a time. 5 minutes to unload.


## Running
Generate data with
```
python3 run_simulation.py
```
The `run_simulation.py` file can be used to modify runtime parameters.

Analyze data with
```
python3 run_analysis.py
```

## Architecture

### Simulation Data Generation

### Main Components
- Simulation management
  - send ticks that represent 1 minute
  - update at "1 minute" intervals

- Have managers for trucks in different states
  - "RouteSitesToStations": Trucks heading from mining sites to unload stations
    - holds trucks in a queue that has 30 positions (1 for each of the next 30 minutes
      since we will "tick" the clock every minute) and each position can hold multiple trucks
  - "RouteStationsToSites": Trucks heading from unload stations to mining sites
    - similar to the one for trucks heading to unload stations
  - Trucks at mining sites
    - holds trucks in a dictionary of timestamps. when a truck "decides" how long it'll be at the
      mining sites, that duration will be added to the current timestamp, and the result will be 
      used to place the truck in the dictionary.
  - Trucks in loading stations ("loading station manager" that controls all loading stations)
    - upon receiving trucks from the route manager, it adds each truck to the loading station with
      the smallest queue (as opposed to a calculated wait time, since the wait time per truck is equal)

- Loading Station
  - contains a queue of trucks, in order of when they're added
  - when adding a truck to the queue, it sets a start timestamp
  - when it receives a timestamp tick, it checks to see if it has been 5 minutes since the start
    timestamp was last set and pops the oldest truck from the queue if able

- Each truck and loading stations can have logs based on the current timestamp they're given

### Analysis