import random
import heapq
import uuid
import sys
import functools

class Peer:
    def __init__(self, id, type, cpu):
        self.id = id
        self.type = type    # slow/fast
        self.cpu = cpu      # low/high
        self.balance = 100
        self.connections = []
        self.transactions = []
        self.blocks = []           # receive blocks

    def connect_to_peer(self, peer):
        self.connections.append(peer)
        peer.connections.append(self)

    def check_connections(self):
        print("Peer", self.id, "is connected to:")
        for peer in self.connections:
            print(" - Peer", peer.id)


class Transaction:
  def __init__(self, id, sender, receiver, amount):
    self.id = id
    self.sender = sender.id
    self.receiver = receiver.id
    self.amount = amount

                                    
class Event:
    def __init__(self, timestamp, callback):
        self.timestamp = timestamp
        self.callback = callback
        
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    

def receive_transaction(generator, frm, to, txn):
    if txn in to.transactions:    # if txn already seen
        return 
    print(f'transaction received from {frm.id} to {to.id}')
    to.transactions.append(txn)
    connected_peers = to.connections
    if frm in connected_peers:
        connected_peers.remove(frm)
    # Check if the txn is valid
    if TxnisValid(generator, txn):
        peer.transactions.append(txn)
        for connected_peer in connected_peers:          # broadcast txn to next connected peers 
            message_length = sys.getsizeof(txn)
            transmission_delay = calculate_latency(to, connected_peer, message_length, fast_peers )
            receive_transaction_callback = functools.partial(receive_transaction, generator= generator,frm=to, to=connected_peer, txn=txn)
            heapq.heappush(event_queue,Event(transmission_delay, receive_transaction_callback))
    else:
        print(f"Transaction {txn.id} is invalid. Not forwarding to connected peers.")
    


def TxnisValid(peer,txn):
    if peer.balance >= txn.amount:
        return True
    return False

def generate_transaction(peer):
    # Generate a transaction for the given 
    connected_peers = peer.connections
    receiver = random.choice(connected_peers)    
    print(f'sender is {peer.id} and receiver is {receiver.id} ' )    
    amount = random.randint(1, 100)
    id = uuid.uuid4()
    txn = Transaction(id, peer, receiver, amount)
    # Schedule the next transaction generation for this peer
    # Send the transaction to the network
    generator = peer
    for connected_peer in connected_peers:
        message_length = sys.getsizeof(txn) * 8
        transmission_delay = calculate_latency(peer, connected_peer, message_length, fast_peers )
        # print('transmission delay ',transmission_delay)
        print('Schedule the receive txn event from the connected peer ', peer.id , ' to ', connected_peer.id)
        receive_transaction_callback = functools.partial(receive_transaction,  generator= generator, frm=peer, to=connected_peer, txn=txn)
        heapq.heappush(event_queue,Event(transmission_delay, receive_transaction_callback))
    print(f"Transaction {txn.id}: {peer.id} pays {receiver.id} - {txn.amount} coins")





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



def peer_connection():
    global peers, num_peers, slow_percent, low_cpu_percent
    peers = []
    for i in range(num_peers):
        type = "slow" if i < num_peers * slow_percent else "fast"
        cpu = "low" if i < num_peers * low_cpu_percent else "high"
        p = Peer(i, type, cpu)
        if type == "slow":
            slow_peers.append(p)
        else:
            fast_peers.append(p)
        peers.append(p)
    

    for i in range(num_peers):
        already_connected = [i]
        connected = peers[i].connections
        for k in connected:
            already_connected.append(k.id)
        if len(already_connected) > 8:
            continue
        for j in range(random.randint(4, 8)):
            try:
                neighbour = random.choice([m for m in range(num_peers) if m not in already_connected])
                already_connected.append(neighbour)
                if len(already_connected) > 8 or len(peers[neighbour].connections) > 7:
                    break
                peers[i].connect_to_peer(peers[neighbour])
            except IndexError:
                break

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
        slow_percent=random.uniform(0, 1)
        low_cpu_percent=random.uniform(0, 1)
        peer_connection()


def calculate_latency(sender, receiver, message_length, fast_peers):
    cij = 100000000 if (sender in fast_peers and receiver in fast_peers) else 5000000
    dij = random.expovariate(96000/cij)
    pij = random.uniform(10e-3, 500e-3)
    latency = pij + message_length/cij + dij
    return latency

num_peers=10
slow_percent=random.uniform(0, 1)
low_cpu_percent=random.uniform(0, 1)
mean_time=10
peers = []
fast_peers = []
slow_peers = []
delay = 1

peer_connection()
print(peers, num_peers, slow_percent, low_cpu_percent)
# Create an event queue
event_queue = []



# Schedule the first transaction generation for each peer
for peer in peers:
    interarrival_time = random.expovariate(1.0 / mean_time)
    generate_transaction_callback = functools.partial(generate_transaction, peer=peer)
    heapq.heappush(event_queue,Event(interarrival_time, generate_transaction_callback ))

# Run the simulation
print('Running simulation')
while event_queue:
    event = heapq.heappop(event_queue)
    event.callback()


for peer in peers:
    print(f'{peer.id} {peer.balance}' )

# if __name__ == "__main__":
#     main(num_peers=5, slow_percent=0.2, low_cpu_percent=0.3, mean_time=10)
