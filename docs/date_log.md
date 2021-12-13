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
- Looked over Iroha: Very simple API with explanations
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
- Started refactoring code and structure so it is easier to understand and change the project eg having one genesis block.

## 2021/11/23
- Refactored directories to have shared genesis block, shared startup script, etc...
- Fixed issue with Iroha4, turns out to be typo in IPv4 address
- Ensured boot up single node and multinode iroha networks
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
- Looked over iroha-python structure, inspecting to see if it is possible to create a malicious peer in this way
	- Seems like using the python API in this way can only get us so far...
	- Maybe some sort of MITM? Add extra transactions to a block and try to get them verified?
- Looked into C++ Iroha structure. VERY dense, difficult to decipher.
	- Possible that crudely altering some files could produce faulty node, but having decent control would require understanding a large amount of the project...
	- Looking into just the YAC C++ could be useful, playing around with consensus
- New plan: Put a hash of a document on the blockchain
	- Looking into the start of abstraction of blockchain to separate claims and validation
	- First step, pre-register documents on a blockchain without revealing the documents
	
## 2021/11/30
- Played around with jupyter notebook in docker containers
- Looked into swi-prolog, and poked about the docker image
- Had a false start using jupyter notebook as a base image, should have used SWIPL as a base image
- Got my own custom image to run jupyter notebook with SWIPL kernel

## 2021/12/1
- Got Stephens swipl container and managed to run it on my machine
- Integrated swipl container into Iroha docker-compose 
- Integrated Iroha package into swipl jupyter kernels
- Got swipl magic files to be hashed and stored on the blockchain

## 2021/12/2
- Worked on SWIPL notebook kernel and Iroha integration
	- Allowed multiple notebooks to be used in a single session
	- Added timestamping so one file can be hashed multiple times (even in same state)
	- Moved Iroha setup to container start, not at first cell runtime

## 2021/12/3
- Added magic %ENV to swipl kernel to change important variables on the fly
- Updated Iroha images to reflect deprecations

## Week 3 Summary
Put plans for node failure testing on hold, focused on implementing file hashing and storage on Iroha blockchain. Got jupyter notebooks running on Docker containers, and loaded SWIPL kernel. Added Iroha functionality to SWIPL kernel to hash magic consultation files and store hash on chain.
---

## 2021/12/6
- Meeting with supervisors
	- Get a very basic "hello, world!" kind of thing running with prolog on blockchain
	- Get communication happening between parties using blockchain verification
	- introduce hidden and open knowledge, both hashed on chain
- Looked into logging and differences in log levels in Iroha
- looked at altering file hashing to track each file individually, by altering domains
- looked into getting state of files by tracking domains and latest hashes

## 2021/12/7
- Got new jupyter-prolog image up and running using the prolog image as a base. This allows for the newest prolog version to be used and update all dependencies in  a single rebuild.
- Changed file hashing to automate domain names as user/file combination, which allows for easy tracking of one file

## 2021/12/8
- Updated SWIPL kernel to work with magic python syntax
- Worked on getting images to display using magic python syntax

## 2021/12/9
- Update SWIPL kernel magic python syntax to accept multi-line (technically block) code
- Added a file custodian to file hashing examples
- Added a blockstore to custodian to cache/remember the assets already seen
- Added threading to blockstore

## 2021/12/10
- Added non-threading option to blockstore to improve performance
- Made blockstore default in custodian
- Cleaned example repos for file hashing and swipl notebook examples
- Made release of file hashing and swipl notebook
- Cleaned VeracityBlockchain repo to remove projects that have grown beyond it

## Week 4 Summary
Improved prolog kernel to add Iroha integration and python support. Gave Kate a platform to run python code in kernel. Added a lot of functionality to file hashing examples. Added ability to specify the domain to hash to, meaning we can track each file as it is updated. Added caching to blockchain queries for file assets, and threading ability to listen for new blocks. Updated examples for file hashing and notebook examples, and published these as releases.
---

## 2021/12/13
- Meeting with supervisors
- Look into other blockchains
	- Indy
	- Hedera
	- Cardano
- Plan: Get a minimal example working for each blockchain, document ease of working with each + pros and cons
- Particular interest in smart contract support on each