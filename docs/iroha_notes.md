# Veracity Spearhead - Summer Project 2021/2022
## Hypderledger Iroha
### Hayden McAlister
---
- Iroha considers TransferAsset with amount=0 to be stateless invalid. This means you cannot transfer 0 amount of an asset. This is a good thing, but not documented anywhere.

- Iroha will happily accept a transaction with the same hash as a previous one. This means that when attempting a replay attack, the first transaction is accepted and processed, while the second transaction (fraudulent) is *also* accepted, but is *not* processed. The returned response code is the same as the first transaction with that hash, like a reminder. But even if receiving "committed" for a replayed transaction, the effect only occurs once.