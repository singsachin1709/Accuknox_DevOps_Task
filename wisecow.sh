#!/usr/bin/env bash

SRVPORT=4499
RSPFILE=response

# Remove old response FIFO and create a new one
rm -f $RSPFILE
mkfifo $RSPFILE

get_api() {
    read line
    echo "$line"
}

handleRequest() {
    # Process the request
    get_api
    mod=$(fortune)

    cat <<EOF > $RSPFILE
HTTP/1.1 200

<pre>$(cowsay "$mod")</pre>
EOF
}

prerequisites() {
    # Check if cowsay and fortune exist
    if ! command -v cowsay >/dev/null 2>&1 || ! command -v fortune >/dev/null 2>&1; then
        echo "Install prerequisites."
        exit 1
    fi
}

main() {
    prerequisites
    echo "Wisdom served on port=$SRVPORT..."

    # Keep container alive and serve requests
    while true; do
        cat $RSPFILE | nc -lN $SRVPORT | handleRequest
        sleep 0.01
    done
}

main

