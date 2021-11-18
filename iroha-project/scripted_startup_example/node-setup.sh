PURPLE='\033[0;35m'
NC='\033[0;0m'
echo -e "${PURPLE}REMOVE PREVIOUS SETUP${NC}"
docker container stop iroha some-postgres
docker container rm iroha some-postgres
docker network rm iroha-network

echo -e "\n${PURPLE}STARTING SETUP${NC}"
docker network create iroha-network
docker volume create blockstore

docker run --name some-postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -p 5432:5432 \
    --network=iroha-network \
    -d postgres:9.5 \
    -c 'max_prepared_transactions=100'

docker run --name iroha \
    -d \
    -e IROHA_POSTGRES_HOST=1 \
    -p 50051:50051 \
    -v $(pwd)/iroha/example:/opt/iroha_data \
    -v blockstore:/tmp/block_store \
    --network=iroha-network \
    -e KEY='node0' \
    hyperledger/iroha:latest

echo -e "\n${PURPLE}FINISHED SETUP${NC}"
docker container ls -a
