# Veracity Spearhead - Summer Project 2021/2022
## Cardano
### Hayden McAlister
---
- Web3 - Supports smart contracts and decentralized applications
- Currency: Ada. 1 Ada = 1,000,000 Lovelace. Also supports tokens
- Proof of Stake - [Ouroboros](https://iohk.io/en/blog/posts/2020/06/23/the-ouroboros-path-to-decentralization/)
    - Stake Pools - "Reliable servers run by operators to which Ada holders can delegate stake to"
        - Is this not a step towards centralization again, now having to trust the "reliable servers" and operators?
- Focus on scalability, see [Hydra](https://iohk.io/en/research/library/papers/hydrafast-isomorphic-state-channels/)
- Self-sustainability an issue for PoS - relies on community development+implementation. Treasury system "controlled by community" (?)
- Seemingly good support for exploration - a GUI web interface to see blocks, transactions, even stake pools
- Good talk about security for new users (although it is VERY funny they describe "writing down your private key passphrase" as a "paper wallet")
- Interesting security for block producers - the verification key has built in expiry time
- Offers a "testnet" 
- Possibly the least helpful FAQ I have seen https://docs.cardano.org/core-concepts/pledging-and-delegation-options/#faqs

---
### Smart Contracts
#### Plutus
A Haskell based smart contract language. Partly on-chain and partly off-chain. Off-chain code is pure Haskell (compiled by GHC), while on-chain code is compiled by Plutus compiler. 
    - The interactive playground seems broken, but will look closer at this later

#### Marlowe
A domain specific language, intended for business people not developers. Embedded in Haskell.

#### Glow
A domain specific language for developing DApps.