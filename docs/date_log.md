# Veracity Blockchain project - Log
## Hayden McAlister

Dates are in YYYY/MM/DD format.
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

## 2021/11/23
- Refactored directories to have shared genesis block, shared startup script, etc...
- Fixed issue with Iroha4, turns out to be typo in IPv4 address
- Ensured boot up singlenode and multinode iroha networks
- Added license to git repo
- Started plans to test multinode network in mundane ways
	- Test connections between nodes
	- Test equality of nodes (can send transaction to any node)
	- Test transactions
	- Test commands (make a domain, user, etc)
	- Test queries
- Start looking at good ways to log outputs of several nodes over time
- Ran into a bug that resulted from giving an ssh key as an argument when I should not have
	- Error messages for Hyperledger (at least Iroha) are default, and not very useful

## 2021/11/24
- Worked more on unit tests of multinode network
	- Enabled manual running of test script
	- Added significant logging, including two logging levels
- Updated IrohaUtils slightly
- Met with supervisor, planned next steps
- Recorded screencasts of test outputs
- Created repo for archive of project and example testing
- Pushed my Iroha image to docker hub

## 2021/11/25
- Started looking into malicious actor actions
	- Wanting to prove that network is resilient against a malicious user trying to break it
- Looking into async, threading packages in python, to quickly send requests from one user to several peers (so the network must deal with several conflicting proposals at the same time)
- Started code for unit testing malicious client actions

## 2021/11/26
- Wrote more tests on malicious clients
- Refactored a lot of code in unit testing, to more easily generate users and improve readability
- Finished malicious client scenarios, and updated unit tests to demonstrate these
- Added final functionality to malicious client testing, including logging

## Week 2 Summary
- Got a full four node network running with docker
- Added unit tests for expected network behavior
- Added unit tests for malicious client behavior
- Added demonstration of running tests

---
## 2021/11/29