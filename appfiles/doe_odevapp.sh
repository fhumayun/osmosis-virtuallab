#!/usr/bin/env bash

cd /app/osmosis 

NOHUP_PID="-0"

function start_osmosis () {
 
    nohup ./bin/osmosis -r &> /dev/null &
    NOHUP_PID="$!" 

}

start_osmosis

# Wait for the node.json and osmosis.json files are created
while [ ! -f config/node.json ] || [ ! -f config/osmosis.json ] 
do
  sleep 2
  echo "Waiting for config files"
done

kill -9 $NOHUP_PID &> /dev/null

NOHUP_PID="-0"

# Pass array as an environment variable
if [ -n "$TCP" ]; then 
    ARR="["
    for x in $TCP; do
      if [ "$ARR" != "[" ]; then
        ARR="$ARR,"
      fi
      ARR="$ARR \"$x\""
    done
    ARR="$ARR ]"

    # Update the osmosis.json file
    jq ".tcp_discovery = $ARR" ./config/osmosis.json > ./config/osmosistmp.json
    mv -f ./config/osmosistmp.json ./config/osmosis.json
fi

# Update the node.json file with the ID rovided
if [ -n "$NODE_ID" ]; then 
  jq '.id = "'$NODE_ID'"' ./config/node.json  > ./config/nodetmp.json
  mv -f ./config/nodetmp.json ./config/node.json
fi

# Update the osmosis.json file to accept http requests
jq '.network.settings.api.http.address="0.0.0.0"' ./config/osmosis.json > ./config/osmosistmp.json
mv -f ./config/osmosistmp.json ./config/osmosis.json

# set hostname with env variable. with a check

while true; do
    clear
    cat log/status.txt

    if ! ps -p $NOHUP_PID  > /dev/null; then
      start_osmosis
      sleep 5
    fi

    sleep 2
done