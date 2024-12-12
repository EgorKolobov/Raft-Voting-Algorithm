import random
import time
import threading


class RaftNode:
    ELECTION_INTERVAL_MIN = 0.15  # Delay in seconds
    ELECTION_INTERVAL_MAX = 0.3
    NETWORK_DELAY_MIN = 0.01
    NETWORK_DELAY_MAX = 0.05
    HEARTBEAT_INTERVAL = 0.1
    TIMEOUT_INTERVAL = 0.05

    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.term = 0
        self.voted_for = None
        self.state = "follower"  # Possible states: follower, candidate, leader
        self.votes_received = 0
        self.election_timeout = random.uniform(RaftNode.ELECTION_INTERVAL_MIN,
                                               RaftNode.ELECTION_INTERVAL_MAX)  # Random timeout
        self.last_heartbeat = time.time()

    def start_election(self):
        """Start election process after detecting the absence of the Leader"""
        self.state = "candidate"
        self.term += 1
        self.voted_for = self.node_id
        self.votes_received = 1  # Vote for self
        print(f"Node {self.node_id} started election for term {self.term}")

        # Request votes from all other nodes
        for node in nodes:
            if node.node_id != self.node_id:
                threading.Thread(target=node.request_vote, args=(self.term, self.node_id)).start()

    def request_vote(self, term, candidate_id):
        """Handle a vote request from a candidate. There is no data log checking for the sake of simplicity."""
        time.sleep(random.uniform(RaftNode.NETWORK_DELAY_MIN, RaftNode.NETWORK_DELAY_MAX))  # Simulate network delay

        if term > self.term:  # Update term and reset state if term is higher
            self.term = term
            self.voted_for = None
            self.state = "follower"

        if self.voted_for is None and self.state == "follower":
            self.voted_for = candidate_id
            print(f"Node {self.node_id} voted for {candidate_id} in term {term}")
            nodes[candidate_id].receive_vote()

    def receive_vote(self):
        self.votes_received += 1
        if self.votes_received > self.total_nodes // 2 and self.state == "candidate":
            self.state = "leader"
            print(f"Node {self.node_id} became leader for term {self.term}")
            self.send_heartbeats()

    def send_heartbeats(self):
        while self.state == "leader":
            print(f"Leader {self.node_id} sending heartbeats")
            self.last_heartbeat = time.time()
            for node in nodes:
                if node.node_id != self.node_id:
                    threading.Thread(target=node.receive_heartbeat, args=(self.term,)).start()
            time.sleep(RaftNode.HEARTBEAT_INTERVAL)  # Send heartbeats every HEARTBEAT_INTERVAL seconds

    def receive_heartbeat(self, term):
        if term >= self.term:
            self.term = term
            self.state = "follower"
            self.last_heartbeat = time.time()

    def check_timeout(self):
        """Follower nodes checking on Leader node"""
        while True:
            if self.state == "follower" and time.time() - self.last_heartbeat > self.election_timeout:
                print(f"Node {self.node_id} timed out, starting election")
                self.start_election()
            time.sleep(RaftNode.TIMEOUT_INTERVAL)  # Check timeout every TIMEOUT_INTERVAL seconds


# Create a cluster of empty nodes. All nodes are followers from the start.
total_nodes = 5
nodes = [RaftNode(i, total_nodes) for i in range(total_nodes)]

# Start timeout checkers for all nodes
for node in nodes:
    threading.Thread(target=node.check_timeout, daemon=True).start()

# Let the simulation run for a while
time.sleep(10)
