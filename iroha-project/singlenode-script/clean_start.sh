PURPLE='\033[0;35m'
NC='\033[0;0m'
echo -e "${PURPLE}REMOVE EXAMPLE DOCKER INFORMATION${NC}"
docker container stop iroha some-postgres
docker container rm iroha some-postgres
docker network rm iroha-project_iroha-network
docker volume rm iroha-project_blockstore
