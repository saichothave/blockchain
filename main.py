import hashlib
import time
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC

# Reference link - https://dev.to/freakcdev297/creating-a-blockchain-in-60-lines-of-javascript-5fka

class Block:
    def __init__(self, timestamp, data = []):
        self.timestamp = timestamp
        self.data = data    # transaction (object of transaction class)
        self.prevHash = ""
        self.nonce = 0
        self.hash = self.getBlockHash()

    def getBlockHash(self):
        data = self.prevHash + str(self.timestamp) + str(self.data) + str(self.nonce)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    
    def miningBlock(self,target):
        while(not self.hash.startswith(''.join(map(str,['0']*(target+1))))):     # target as per mentioned in Satoshi's White Paper
            self.nonce += 1
            self.hash = self.getBlockHash()
            break

    def hasValidTransactions(self, chain):
        for block in chain:
            if block.data.isValidTransaction(block.data, chain):
                print('valid')
                continue
            return False

class BlockChain:
    def __init__(self):
        initialCoinRelease = Transaction(mint_public_key, holder_public_key, 2000)    # releasing coins in the market
        genesisBlock = Block(str(time.time()), [initialCoinRelease])
        print('genesis block ',genesisBlock)
        self.chain = [genesisBlock]
        self.target = 1
        self.transactions = []
        self.reward = 50

    def getLastBlock(self):
        return self.chain[len(self.chain)-1]

    def addBlocktoChain(self,block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getBlockHash()
        block.miningBlock(self.target)
        print('block adding to chain ',block)
        self.chain.append(block)

    def isValidChain(self):
        for i in range(1,len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i-1]

            if currentBlock.prevHash != prevBlock.hash or currentBlock.hash != currentBlock.getBlockHash() or not currentBlock.hasValidTransactions(self.chain):
                return False

        return True
    
    def showChainTransactions(self):
        for i in range(len(self.chain)):
            print(self.chain[i].data)

    def addTransaction(self, transaction):
        print('transaction ',transaction.__dict__)
        if transaction.isValidTransaction(transaction, self):
            self.transactions.append(transaction)
            print('transaction added')
    

    def getBalance(self,address):
        balance = 0
        for i in range(len(self.chain)):
            block = self.chain[i]
            for tx in (block.data):
                if tx.frm == address:
                    balance -= tx.amount

                if tx.to == address:
                    balance += tx.amount

        return balance    
    
    def mineTxns(self, rewardAddr):
        rewardTxn = Transaction(mint_public_key, rewardAddr, self.reward)        # more money gets created from mint_public_key 
        rewardTxn.signTxn(mint_public_key, mint_private_key)
        self.transactions.append(rewardTxn)
        print('reward txn ',rewardTxn)
        self.addBlocktoChain(Block(str(time.time()), self.transactions ))
        self.transactions = []

    

class Transaction:
    def __init__(self, frm, to, amount):
        self.frm = frm
        self.to = to
        self.amount = amount
        

    def signTxn(self, public_key, private_key):
        if public_key == self.frm:
            message = str(self.frm) + str(self.to) + str(self.amount)
            message = bytes(message, 'utf-8') 
            self.transation_hash = SHA256.new()
            self.transation_hash.update(message)
            self.signature = DSS.new(private_key, 'fips-186-3').sign(self.transation_hash)

    def isValidTransaction(self, txn, chain):
        try:
            DSS.new(txn.frm, 'fips-186-3').verify(self.transation_hash, self.signature)      # signature verification
            print("The signature is valid.")
        except ValueError:
            print("The signature is invalid.")
            return False
            
        return ((txn.frm is not None) 
                 and (txn.to is not None) 
                      and (txn.amount is not None)
                            and (chain.getBalance(txn.frm) >= txn.amount or txn.frm == mint_public_key))





mint_private_key = ECC.generate(curve='P-256')
mint_public_key = mint_private_key.public_key()
holder_private_key = ECC.generate(curve='P-256')
holder_public_key = holder_private_key.public_key()

SampleBlockChain = BlockChain()
sk2 = ECC.generate(curve='P-256')
pk2 = sk2.public_key()

print(SampleBlockChain.getBalance(mint_public_key))
print(SampleBlockChain.getBalance(holder_public_key))

print('\n------------------ Creating Transaction ------------------')
txn1 = Transaction(holder_public_key, pk2, 100)
print(txn1)
print('\n------------------Transaction Created Successfully ------------------')

print('#'*100)

print('\n----------------------Signing Transaction------------------------------')
txn1.signTxn(holder_public_key,holder_private_key)
print('----------------------Signed Successfully ---------------------')

print('#'*100)


print('\n----------------------Adding Transaction------------------------------')
SampleBlockChain.addTransaction(txn1)
print('----------------------Added Successfully ---------------------')

print('#'*100)

print('\n----------------------Mining Transaction------------------------------')
SampleBlockChain.mineTxns(holder_public_key)
print('----------------------Mined Successfully ---------------------')


sk3 = ECC.generate(curve='P-256')
pk3 = sk3.public_key()

print('\n------------------ Creating Transaction ------------------')
txn1 = Transaction(pk2, pk3, 50)
print(txn1)
print('\n------------------Transaction Created Successfully ------------------')

print('#'*100)

print('\n----------------------Signing Transaction------------------------------')
txn1.signTxn(pk2,sk2)
print('----------------------Signed Successfully ---------------------')

print('#'*100)


print('\n----------------------Adding Transaction------------------------------')
SampleBlockChain.addTransaction(txn1)
print('----------------------Added Successfully ---------------------')

print('#'*100)

print('\n----------------------Mining Transaction------------------------------')
SampleBlockChain.mineTxns(pk3)
print('----------------------Mined Successfully ---------------------')



print(SampleBlockChain.getBalance(holder_public_key))
print(SampleBlockChain.getBalance(pk2))
print(SampleBlockChain.getBalance(pk3))
print(SampleBlockChain.getBalance(mint_public_key))
