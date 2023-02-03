import random
import heapq
import uuid
import sys
import functools
import time

class Peer:
    def __init__(self, id, type, cpu, hashing_power, chain=[]):
        self.id = id
        self.type = type    # slow/fast
        self.cpu = cpu      # low/high
        self.hashing_power = hashing_power
        self.balance = 0
        self.connections = []
        self.transactions = []
        self.chain = chain  

    def connect_to_peer(self, peer):
        self.connections.append(peer)
        peer.connections.append(self)
    
    def disconnect_from_peer(self, peer):
        self.connections.remove(peer)
        peer.connections.remove(self)

    def check_connections(self):
        print("Peer", self.id, "is connected to:")
        for peer in self.connections:
            print(" - Peer", peer.id)

    def getBalance(self):
        balance = 0

        print('len(self.chain)',len(self.chain))
        for i in range(len(self.chain)):
            txns = self.chain[i].transactions
            print('txns ',txns)
            for txn in txns:
                print('txn amnt',txn.sender.id , txn.receiver.id, self.id, txn.amount)
                if txn.sender.id == self.id:
                    balance= balance - txn.amount
                    print('sender ',txn.sender.id, 'balance= ',balance)

                elif txn.receiver.id == self.id:
                    balance = balance + txn.amount
                    print('receiver ',txn.receiver.id, 'balance= ',balance)

        print('balance of ', self.id, ' is', balance)
        return balance




class Transaction:
    def __init__(self, id, timestamp, sender, receiver, amount):
        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def isValid(self,peer):
        # print(f'peer {peer.id} transaction amount is {self.amount} and size is {sys.getsizeof(self)} bytes')
        if peer.balance >= self.amount and sys.getsizeof(self) <= 1024:
            return True
        return False

                                    
class Event:
    def __init__(self, timestamp, callback):
        self.timestamp = timestamp
        self.callback = callback
        
    def __lt__(self, other):
        return self.timestamp < other.timestamp
    

class Block:
    def __init__(self, id, timestamp, prevBlock, transactions):
        self.id = id
        self.timestamp = timestamp
        self.prevBlock = prevBlock
        self.transactions = transactions

        
    def hasValidTransactions(self):
        for tx in self.transactions:
            if tx.amount > tx.sender.getBalance():
                return False
        return True
    
    def broadcastBlock(self, miner, earlier_len):
        if len(miner.chain) > earlier_len:
            print("Discard Block")
            return False
        if len(miner.chain) == earlier_len:
            for tx in self.transactions:    # removing transactions from miner's transaction pool
                miner.transactions.remove(tx)
            
            coinbaseTxn = Transaction(uuid.uuid4(),time.time(), money_creater, miner, 50)
            self.transactions.append(coinbaseTxn)
            miner.chain.append(self)
            print(miner.transactions)
            print("Broadcast block")
            # connected_peers = miner.connections
            # for peer in connected_peers:
            #     if self.hasValidTransactions():
            #         print('Block validated')

                
    
    def miningBlock(self, miner):
        print('transactions for mining block is ', self.transactions, len(self.transactions))
        mean = I/miner.hashing_power
        Tk = random.expovariate(mean)
        print('mining interarrival time ',Tk)
        earlier_chain_length = len(miner.chain)
        broadcastBlock_callback = functools.partial(self.broadcastBlock, miner = miner, earlier_len= earlier_chain_length)
        heapq.heappush(event_queue,Event(Tk  , broadcastBlock_callback))
        
    

def receive_transaction(generator, frm, to, txn):
    if txn in to.transactions:    # if txn already seen
        return 
    print(f'transaction received from {frm.id} to {to.id} where generator is {generator.id}')
    connected_peers = to.connections.copy()

    if frm in connected_peers:
        connected_peers.remove(frm)
    # Check if the txn is valid
    if generator.getBalance() >= txn.amount:
        to.transactions.append(txn)
        for connected_peer in connected_peers:          # broadcast txn to next connected peers 
            message_length = sys.getsizeof(txn)
            transmission_delay = propagation_delay(to, connected_peer, message_length, fast_peers )
            receive_transaction_callback = functools.partial(receive_transaction, generator= generator,frm=to, to=connected_peer, txn=txn)
            heapq.heappush(event_queue,Event(transmission_delay , receive_transaction_callback))
    else:
        print(f"Transaction {txn.id} is invalid. Not forwarding to connected peers.")
    




def generate_transaction(peer):
    # Generate a transaction for the given 
    connected_peers = peer.connections.copy()
    print(peer.id,connected_peers)
    receiver = random.choice(connected_peers)    
    print(f'sender is {peer.id} and receiver is {receiver.id} ' )    
    amount = random.randint(1, 100)
    id = uuid.uuid4()
    txn = Transaction(id, time.time(), peer, receiver, amount)
    # Schedule the next transaction generation for this peer
    # Send the transaction to the network
    generator = peer
    for connected_peer in connected_peers:
        message_length = sys.getsizeof(txn) * 8
        transmission_delay = propagation_delay(peer, connected_peer, message_length, fast_peers )
        # print('transmission delay ',transmission_delay)
        print('Schedule the receive txn event from the connected peer ', peer.id , ' to ', connected_peer.id)
        receive_transaction_callback = functools.partial(receive_transaction,  generator= generator, frm=peer, to=connected_peer, txn=txn)
        heapq.heappush(event_queue,Event(transmission_delay  , receive_transaction_callback))
    print(f"Transaction {txn.id}: {peer.id} pays {receiver.id} {txn.amount} coins")





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
    # if num_peers < 5:
    #     return "Atleast 5 Peers required to form a P2P Network ( Since atleast 4 peers has to be connected to any peer)"
    peers = []
    num_low_cpu =  num_peers * low_cpu_percent
    num_high_cpu = num_peers - num_low_cpu
    l_hp = 1/(num_low_cpu + 10*num_high_cpu)
    h_hp = 10 * l_hp
    initial_transactions = []
    for i in range(num_peers):
        type = "slow" if i < num_peers * slow_percent else "fast"
        cpu = "low" if i < num_low_cpu else "high"
        p = Peer(i, type, cpu, l_hp) if cpu == "low" else Peer(i, type, cpu, h_hp)
        initial_transactions.append(Transaction(uuid.uuid4(), time.time() , money_creater, p, 1000))
        slow_peers.append(p) if type=="slow" else fast_peers.append(p)
        peers.append(p)

    genesis_blk = Block(uuid.uuid4(),time.time(), None, initial_transactions)
    print('genesis blk ',genesis_blk)
    for p in peers:
        print('peer ',p.id)
        p.chain = [genesis_blk]

   
    
    for i in range(num_peers):
        already_connected = [i]
        connected = peers[i].connections.copy()
        for k in connected:
            already_connected.append(k.id)
        while len(peers[i].connections) < 4:
            try:
                neighbour = random.choice([m for m in range(num_peers) if m not in already_connected])
                already_connected.append(neighbour)
                if len(peers[neighbour].connections) >= 8:
                    continue
                peers[i].connect_to_peer(peers[neighbour])
            except IndexError:
                break
        while len(peers[i].connections) > 8:
            disconnect = random.choice(peers[i].connections)
            peers[i].disconnect_from_peer(disconnect)





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


def propagation_delay(sender, receiver, message_length, fast_peers):
    cij = 100000000 if (sender in fast_peers and receiver in fast_peers) else 5000000
    dij = random.expovariate(96000/cij)
    pij = random.uniform(10e-3, 500e-3)
    delay = pij + message_length/cij + dij
    return delay

num_peers=3
slow_percent=random.uniform(0, 1)
low_cpu_percent=random.uniform(0, 1)
mean_time=10
I = 600
peers = []
fast_peers = []
slow_peers = []

#initial coin 
money_creater = Peer(-1, "fast", "high", 0)
money_creater.balance = 9000000
money_holder = Peer(-2, "fast", "high", 0)

peer_connection()
print(peers, num_peers, slow_percent, low_cpu_percent)
# print(peers[0].chain)

# Create an event queue
event_queue = []

# Schedule the first transaction generation for each peer
for peer in peers:
    interarrival_time = random.expovariate(1.0 / mean_time)
    generate_transaction_callback = functools.partial(generate_transaction, peer=peer)
    heapq.heappush(event_queue,Event(interarrival_time, generate_transaction_callback ))

# print(len(event_queue))
# print(peers[0].transactions)
# block1 = Block(uuid.uuid4(), time.time(), peers[0].chain[len(peers[0].chain)-1].id,peers[0].transactions)
# miningBlock_callback = functools.partial(block1.miningBlock, miner=peers[0])
# heapq.heappush(event_queue,Event(I, miningBlock_callback ))

# Run the simulation

print('Running simulation')
while event_queue:
    event = heapq.heappop(event_queue)
    event.callback()
# print('block1 ',block1.transactions)
# print(peers[0].chain[1].transactions)

# for p in peers:
#     print(p.chain)

print(peers[0].id,peers[0].getBalance())
print(peers[0].id, len(peers[0].transactions), peers[0].transactions )
# for peer in peers:
#     print(f'{peer.id} {peer.balance}' )

