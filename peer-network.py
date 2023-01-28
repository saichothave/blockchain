import random
import heapq
import time

class Peer:
    def __init__(self, id, type, cpu):
        self.id = id
        self.type = type    # slow/fast
        self.cpu = cpu      # low/high
        self.balance = 0
        self.connections = []
        self.blocks = []           # receive blocks

    def connect_to_peer(self, peer):
        self.connections.append(peer)
        peer.connections.append(self)

    def check_connections(self):
        print("Peer", self.id, "is connected to:")
        for peer in self.connections:
            print(" - Peer", peer.id)

    

                                    
class Event:
    def __init__(self, timestamp, callback):
        self.timestamp = timestamp
        self.callback = callback
        
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    
def send_block(peer, block):
    # Get a list of the peer's connected peers
  
    connected_peers = [p for p in peers if peer in p.connections]
    for connected_peer in connected_peers:
        # Check if the connected peer is slow or fast
        print(f'sending block from {peer.id} to {connected_peer.id}')
        if connected_peer.type == "slow":
            delay = random.expovariate(1.0 / slow_peer_delay)
        else:
            delay = random.expovariate(1.0 / fast_peer_delay)

        # Schedule the receive block event for the connected peer
        print('Schedule the receive block event for the connected peer', connected_peer.id, 'from ', peer.id)
        event_queue.append(Event(delay, receive_block(connected_peer, block)))

def receive_block(peer, block):
    # Get a list of the peer's connected peers
    if block in peer.blocks:    # if block already seen
        return
    connected_peers = [p for p in peers if peer.id in p.connections]
    for connected_peer in connected_peers:
        # Check if the connected peer is slow or fast
        if connected_peer.type == "slow":
            # Introduce delay in receiving the block
            time.sleep(slow_peer_delay)
        else:
            time.sleep(fast_peer_delay)

    # Add the block to the peer's block list
    peer.blocks.append(block)
    print(f"Peer {peer.id} received block {block}.")
    # Check if the block is valid
    # if block.is_valid():
    #     # If the block is valid, forward it to all connected peers
    #     for peer in peer.connected_peers:
    #         peer.receive_block(block)
    # else:
    #     print(f"Block {block.id} is invalid. Not forwarding to connected peers.")
    receive_block(peer,block)
    print('block received at ',peer.id)


def generate_transaction(peer):
    # Generate a transaction for the given peer
    # Generate a random amount for the transaction
    amount = random.randint(1, 100)
    print('amount ',amount)

    # Update the peer's balance
    peer.balance += amount

    # Schedule the next transaction generation for this peer

    # Send the transaction to the network
    block = {"sender": peer.id, "amount": amount}
    send_block(peer, block)




def check_connected_graph(peers):
    # Create a queue for BFS
    queue = []
    # Create a visited array
    visited = [False for _ in range(len(peers))]
    # Starting from the first peer
    queue.append(peers[0])
    visited[0] = True
    # Perform BFS
    while queue:
        current_peer = queue.pop(0)
        for peer in current_peer.connections:
            if not visited[peer.id]:
                queue.append(peer)
                visited[peer.id] = True
    # If all the peers are visited, it's a connected graph
    if all(visited):
        return True
    else:
        return False

# def main(num_peers, slow_percent, low_cpu_percent, mean_time):
    # Initialize the network with the given parameters
num_peers=random.randint(4, 8)
slow_percent=random.uniform(0, 1)
low_cpu_percent=random.uniform(0, 1)
mean_time=10
peers = []
slow_peer_delay = 100000
fast_peer_delay = 5000
print(peers, num_peers, slow_percent, low_cpu_percent)

def peer_connection():
    global peers, num_peers, slow_percent, low_cpu_percent
    peers = []
    for i in range(num_peers):
        type = "slow" if i < num_peers * slow_percent else "fast"
        cpu = "low" if i < num_peers * low_cpu_percent else "high"
        peers.append(Peer(i, type, cpu))

    for i in range(num_peers):
        for j in range(i+1,num_peers):
            if random.random()<0.5:
                peers[i].connect_to_peer(peers[j])

    for p in peers:
        print('peer')
        print(p.__dict__)
        p.check_connections()

    # check if the formed peer connection is connected graph
    if check_connected_graph(peers):
        print("The peers are connected and form a connected graph.")
    else:
        print("The peers are not connected and do not form a connected graph.")
        print("reform the connection")
        num_peers=random.randint(4, 8)
        slow_percent=random.uniform(0, 1)
        low_cpu_percent=random.uniform(0, 1)
        peer_connection()


peer_connection()
print(peers, num_peers, slow_percent, low_cpu_percent)
# Create an event queue
event_queue = []



# Schedule the first transaction generation for each peer
for peer in peers:
    interarrival_time = random.expovariate(1.0 / mean_time)
    print('interarrival time ', interarrival_time)
    event_queue.append(Event(interarrival_time, generate_transaction(peer)))
    print('event generated')

# # Run the simulation
# while event_queue:
#     event = heapq.heappop(event_queue)
#     print(event)
#     event.callback()
        

# if __name__ == "__main__":
#     main(num_peers=5, slow_percent=0.2, low_cpu_percent=0.3, mean_time=10)
