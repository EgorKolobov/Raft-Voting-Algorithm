# Raft Voting Algorithm Simulation

This project is a Python-based simulation of the voting process in the Raft consensus algorithm. It demonstrates how leader elections occur in a distributed system and explores potential issues such as split votes and network delays.

## Features
- Randomized election timeouts to prevent split votes.
- Leader election process with vote requests and majority-based selection.
- Heartbeat mechanism to maintain leadership.
- Simulated network delays to illustrate real-world challenges.

## How It Works
1. **Nodes and Roles**: Each node in the cluster can act as a follower, candidate, or leader.
2. **Election Process**: When a node times out without receiving a heartbeat, it transitions to a candidate and starts an election by requesting votes from other nodes.
3. **Leader Selection**: The node that receives votes from the majority of nodes becomes the leader and begins sending heartbeats to maintain authority.
4. **Heartbeat Handling**: If a follower receives a heartbeat, it resets its election timeout, ensuring the leader's role remains stable.

## Requirements
- Python 3.7 or higher

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/EgorKolobov/Raft-Voting-Algorithm.git
   ```

## Usage
1. Run the script to simulate the Raft voting algorithm:
   ```bash
   python main.py
   ```
2. Observe the console output to see the election process, votes, and leadership transitions.
## Configurations
- Modify the default timeouts in the script:
  ```python
  ELECTION_INTERVAL_MIN = 0.15  # Minimum election timeout in seconds
  ELECTION_INTERVAL_MAX = 0.3  # Maximum election timeout in seconds
  ...
  ```
- Change the number of nodes by adjusting the `total_nodes` variable.

## Potential Improvements
- Add persistent state (e.g., disk storage) to simulate real-world use cases.
- Include log replication to demonstrate full Raft functionality.
- Introduce fault injection to test resilience under node failures.

## Acknowledgments
This implementation is inspired by the Raft consensus algorithm described by Diego Ongaro and John Ousterhout in their paper *"In Search of an Understandable Consensus Algorithm".*

