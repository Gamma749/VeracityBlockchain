#!/bin/bash

docker container rm deepnote-swipl

docker run \
	-p 8888:8888 \
	-v $(pwd)/notebooks:/notebooks \
	--name deepnote-swipl \
	-it gamma749/deepnote-swipl run-notebook
