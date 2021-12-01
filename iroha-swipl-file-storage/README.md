# SWIPL Magic File Iroha File Hash Example

## Prerequisites
Ensure that your machine runs docker and docker-compose.

## Network Setup
From the multinode-network directory, run
`./manage-network up`
to start the iroha containers. Run
`./manage-network down`
to destroy those containers when finished.
Run
`./manage-network (pause|unpause)`
to pause or unpause the network respectively.

## Running this project
While in development, running `./manage-network up` will totally rebuild the docker image for the `notebook-swipl` container. This is because sometimes using docker-compose and dockerfiles can lead to the container not updating between tests. Note that this can be expensive, but should be removed once the image is in a stable state.

After running `./manage-network up`, a log from the `notebook-swipl` container will be printed to the terminal with a link to the jupyter notebook. This notebook will have a prolog kernel available.

Notebooks are saved to persistent storage on the host in the `network/swipl/notebooks` directory. 

Using magic file notation (putting `%file: filename.pl` at the top of a prolog cell), that file will be hashed and stored on the Iroha blockchain running on the iroha containers. This provides a record of what files were activated and when, which could be used to detect inconsistencies in a prolog environment.

A log of the blockchain is stored after each new file is stored on the chain. The logs are stored in `network/swipl/notebooks/logs` due to a quirk in how jupyter notebook kernels work.

## TODO
Currently, if a file is in state A, then changes to state B, then back to state A, the second iteration of state A will not be stored on the chain. This is because the hashing process cannot follow the state of a single file, so it does not know that the state B hash is an update to the same file. This could be fixed/hacked together by adding a timestamp to the file at save time.