
function up(){

    docker-compose -f network/docker-compose.yaml up -d
    
    echo waiting 3m for start up process
    sleep 3m
    echo finishing of start up process  
}

function pause(){
    docker-compose -f network/docker-compose.yaml pause
}

function unpause(){
    docker-compose -f network/docker-compose.yaml unpause
}
function down(){

    docker-compose -f network/docker-compose.yaml down --volumes --remove-orphans
}

function restart(){
    down
    up
}

"$@"
