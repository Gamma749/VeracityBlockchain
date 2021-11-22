# Hyperledger-Iroha-Singlenode-Network

## Prerequisites
Your machine will need Docker.

Also ensure that you have cloned the iroha project git repo in this directory, as the example situation will be loaded.

## Running this example
Run `./node-setup.sh` to stop any previous containers and create new iroha and postgres containers on a network. 
After waiting for the containers to spin up, you can investigate the iroha container with `docker exec -it iroha /bin/bash`

When you are done with the example, run `docker stop iroha some-postgres` to stop these containers (but keep the blockstore volume and network). Alternatively, you can run `./node-shutdown` to remove the network, blockstore, and containers.

Notice that if you have running containers and manually shut them down with `docker stop`, you will keep the blockstore volume. Because `node-setup` does not delete the blockstore volume, this volume will be reused if you run `./node-setup` again. This means all your previous transactions will be available on a new container. If this is not the behavior you want, you can manually remove the blockstore volume or you can run `./node-shutdown` which takes care of this for you.