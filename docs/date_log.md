# Veracity Blockchain project - Log
## Hayden McAlister
---
## 2021/11/15
- Familarised self with blockchain, watched MIT course on blockchain technology

## 2021/11/16
- Looked over consensus alogrithims, looked briefly at hyperledger projects
  (particularly Indy)
- Took long notes on Indy API

## 2021/11/17
- Meeting with David + Stephen, discussed veracity in project and goals
- Looked over Sawtooth: Very opaque API but seems powerful + modular
- Looked over Iroha: Very simple API with explainations
- Got Iroha docker container running

## 2021/11/18
- Looked at YAC protocol paper
	- Looked at Nakamoto consensus and Byzantine vs Practical Byzantine fault tolerance
- Worked on using iroha docker container
	- Got example working using setup scripts, was able to use iroha-cli to add assets and transfer about
	- Created an image with python3 and iroha python package 
	- Created docker compose yaml file to easily boot iroha example with postgres container too
	- Looked into using python library, analysed code

## 2021/11/19
- Looked into python sdk for Iroha more, reading over functions offered and taking notes
	- Look over all commands possible
	- Understand structure of python files and how commands move through into blockchain
- Started plans for migration to new computer
- Got own python files with transactions and queries running over top of example single node network
	- Now to look at developing own genesis block and users+roles
	- Look into multinode networks

## Week 1 Review
Got started on the project, began looking into blockchain and blockchain projects. Decided on using Hyperledger Iroha to start with, and began looking over documentation for configurations and Python API. Got an example multinode network running.

---
## 2021/11/22
- Looked closer at configurations of Iroha, especially at docker configuration files
	- Looking for options that will be useful when testing/demonstrating, like timeouts and quorums
- Got another node running in the docker compose, for a total of four and a fault tolerance of one
	- iroha4 is misbehaving, determining why?
- Started refactoring code and structure so it is easier to understand and change the project eg having one gensis block.
