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