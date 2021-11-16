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

In the network as a whole, there are several different nodes that exist (in Bitcoin example, how do these change in other blockchains):
- Full Nodes: Store full blockchain and can validate transactions (e.g. knows how much is in each wallet)
- Pruning Nodes: Prune transactions after validation and aging
- Lightweight Nodes: Store headers only (also SPV nodes)
- Miners: Perform PoW and create new blocks - not necessarily Full Nodes as pool operators can do that


## Trust
Because all blocks reference backwards to the genesis block, it is possible to trace all trust back to this genesis block (where all nodes should agree, as nothing has yet occurred) by checking hashes and Merkle trees. Thus all trust is traced back to the initial trust event.

Trust is kept at a deeper level by cryptographic primitives of hash functions and encryption, which are mathematically "good enough" (not guaranteed) to give unique outputs for each input. If a collision (or worse) occurs this can undermine the effectiveness of a blockchain as trust cannot be ensured.

## Permissioned vs Permissionless
Permissioned systems have nodes that have been validated and trusted before they are allowed to write new blocks. In this way, there is little need for consensus algorithms, as the number of nodes is usually a lot lower and there is no need to prove you have some stake in the system. However, this is still a need to address faults (particularly Byzantine faults) and we may want to investigate how we remove trust in a permissioned system when that trust is lost (due to an incorrect node or malicious actor). Hyperledger is a permissioned system.

Permissionless systems have nodes which are *not* validated and hence must prove their work before being trusted, requiring consensus protocols. Bitcoin is an example, and permissionless systems generally scale better (at least from the user joining aspect, quantifying how the extra overhead of consensus protocols impacts this is difficult).

## Smart Contracts
Get some code to run on the blockchain
Nick Szabo, 1996: "A set of promises specified in digital form, including protocols, within which the parties perform on those promises"
Basically code on a blockchain, executed when a condition is met. Some people are using these in place of hard/traditional contracts but this leaves some legal holes that may need to be avoided. Traditional contracts are only as valuable as enforcement (enforced by the state) so illegal contracts are worthless. Smart contracts are enforced by computing (code is seen by parties on the blockchain and is agreed to, and that code will be executed by a correct node when the contract is triggered). If something goes wrong, we must defer back to the state, however!

Some claim smart contracts could replace legal system in places where legal system is not great (e.g. third world). This seems overly trusting.
Smart contracts could remove obscurity or ambiguity from contracts. Could be good clarity (although a layperson may have no better chance of understanding it) but that is not always a good thing

A smart contract must:
- Not have arbitrary inputs (emotion, opinion)
- Have a social context (cannot have only a single participant)
- inputs must be material, mesurable, and exchangable

Contract Lifecycle:
1. Negotiation. All parties understand contract terms. Requires common
   knowledge/common ground, which can only be updated by "grounding":
   where parties come to new common ground
2. Storage. A contract is stored somewhere and can be checked and monitored
3. Execution. The contract terms are executed and followed through on in
   full.
4. Dispute Resolution. Any disputes about the contract execution can be
    - Adjudicative Resolution: judge, jury, or arbitrator determines outcome of
      contract
    - Consensual Resolution: Negotation or collaborative law, where parties try
      to reach an agreement

A smart contract may implement this lifecycle (Negotiation is creation of the
contract, storage on the blockchain, automatic execution). However, more
research is needed into automatic executation for possible vulenrabilities
(especially for contract parties and blockchain health). A smart contract may
not perform well in the Dispute Resolution step, as it is automatically
executed and blockchain (being append only) cannot undo the contract without
*another smart contract*. Both resolution types suffer from this.

## Consensus and Consensus Protocols
- Generally support the longest chain, as this removes forks and prevents inconsistent groups forming.
- Consensus protocols allow for distributed networks to all agree on something (here, a block). In blockchain we use consensus protocols to choose who creates the next block
  - Proof of Work: miners compete to find solution to a computationally intensive NP-problem (so it is hard to solve but easy for other nodes to verify). In Bitcoin: change a nonce value in header of block to find hash of block with a certain amount of leading 0's. Miners have incentive to mine in the form of native currency rewards (e.g. some bitcoin per mined block).
    - PoW uses a huge amount of energy on effectively no useful work, so it has massive environmental impacts.
  - Proof of Stake: some nodes are picked out from all nodes as the block creators of the next block. These nodes create the next block and sign it, distributing the new block across the network.
    - Because the creator nodes are chosen (randomly) it means there is no need for intense races to make the next block (PoW). There is also no need for incentives, as sometimes being a block creator is part of the contract each user agrees to when using the blockchain.
    - How to choose a block creator? How do we determine stake in an arbitrary system?
    - What if a block creator suffers a Crash Fault? What if a block creator is malicious? 
  - Proof of Authority: 
  - Proof of Activity:
  - Proof of Burn: 
  - Proof of Capacity:
  - 
## Attacks and Issues
- Malicious actors on the blockchain can exploit it, such as by giving incorrect information (Byzantine fault) or by creating false events(?). How to identify malicious nodes? How to ignore incorrect messages? How to punish malicious actors (e.g. ban from blockchain)
- Joining a blockchain requires knowing all blocks back to the genesis block. We can somewhat cut down on download size by only looking at headers however then we would have to trust further to get the current state of the system from others, e.g. we get told how much each wallet contains.
  - If a malicious node gave a new node a false copy of a blockchain, it is possible to either induct the new node into a malicious attack or to compromise the blockchain by introducing an incorrect node. Must find a way to ensure download is correct.
    - Maybe we can download from enough nodes that we are statistically likely (or guaranteed) to get the majority consensus as correct?
- Crash Fault: When a node goes offline. Usually not a big issue, as ledger is distributed, so other nodes continue to work. May be an issue if node drops out during non-idle periods (e.g. if using proof of stake and a node is selected as a block creator, but dies?)
  - Also ensure that crash faults do not significantly impact malicious factor
- Byzantine Fault: When a node is still online and communicating but is in an incorrect state relative to the consensus. How to correct the node? Or how to identify the incorrect node from all nodes when receiving messages? If many incorrect nodes, what is the fault tolerance?
- Forks: If a blockchain is forked then there may be two or more groups that think they are consistent within a group but are inconsistent between groups. If a fork is not immediately recognized then it may be very difficult to reconcile the forks.
- Network attack: If a malicious actor can control the network between nodes and tamper with communication here, it is possible to control the blockchain. We could combat this with TLS or other encryption of messages, or maybe digital signatures. 
- Privacy: Consider something like GDPR which allows for people to request (see: demand) their private information to be deleted. In blockchain, an append only system, deletion doesn't truly exist. What to do here?
