# Veracity Spearhead - Summer Project 2021/2022
## Blockchain
### Hayden McAlister
---
# Goals
- Veracity spearhead wants a demonstration of blockchain in this context of veracity and provenance. Essentially, aim to implement a blockchain that allows for tracking of facts among a (distributed) group and can track where these facts and beliefs of facts came from.
- In the long run, getting Kate's event calculus to run on the blockchain would be interesting, particularly in looking at how to undo, fix, or identify inconsistencies between nodes
- Veracity spearhead wants, at the end of the day, a demonstration of blockchain working. This could come from:
  - Docker containers interacting using blockchain, maybe scripting different events and issues?
  - Animation of blockchain in action, along with an explanation? Maybe using Manim?
- Must develop own use case for application: make problem and solve it!
- 
# Blockchain
## Anatomy
A blockchain is a chain of blocks. The initial block (the genesis block) references nothing and is taken as the root, consistent state between all nodes. Each subsequent block references the previous block to ensure a chain of trust and verification exists.

A single block in the chain consists of a header and a body of events that occurred on this block. Each event is hashed and placed into a Merkle tree, the root of which is placed into the header, although this is not the only way to verify all transactions. Using a Merkle tree does make it very easy to identify which transaction has been tampered with quickly. Common header fields include the previous block hash (required), the Merkle tree root hash (or other verification of events), a timestamp (although not needed if blocks are in order). Other fields include a version, a nonce (number appended to get hash value required, particularly proof of work). Once a block is created, it is added to the blockchain and distributed to all other nodes. Other nodes can verify using the nonce and previous hash.

## Trust
Because all blocks reference backwards to the genesis block, it is possible to trace all trust back to this genesis block (where all nodes should agree, as nothing has yet occurred) by checking hashes and Merkle trees. Thus all trust is traced back to the initial trust event.

Trust is kept at a deeper level by cryptographic primitives of hash functions and encryption, which are mathematically "good enough" (not guaranteed) to give unique outputs for each input. If a collision (or worse) occurs this can undermine the effectiveness of a blockchain as trust cannot be ensured.

## Consensus and Consensus Protocols

## Attacks and Issues
- Malicious actors on the blockchain can exploit it, such as by giving incorrect information (Byzantine fault) or by creating false events(?). How to identify malicious nodes? How to ignore incorrect messages? How to punish malicious actors (e.g. ban from blockchain)
- Joining a blockchain requires knowing all blocks back to the genesis block. We can somewhat cut down on download size by only looking at headers however then we would have to trust further to get the current state of the system from others, e.g. we get told how much each wallet contains.
  - If a malicious node gave a new node a false copy of a blockchain, it is possible to either induct the new node into a malicious attack or to compromise the blockchain by introducing an incorrect node. Must find a way to ensure download is correct.
    - Maybe we can download from enough nodes that we are statistically likely (or guaranteed) to get the majority consensus as correct?
- Crash Fault: When a node goes offline. Usually not a big issue, as ledger is distributed, so other nodes continue to work. May be an issue if node drops out during non-idle periods (e.g. if using proof of stake and a node is selected as a block creator, but dies?)
  - Also ensure that crash faults do not significantly impact malicious factor
- Byzantine Fault: When a node is still online and communicating but is in an incorrect state relative to the consensus. How to correct the node? Or how to identify the incorrect node from all nodes when receiving messages? If many incorrect nodes, what is the fault tolerance?

