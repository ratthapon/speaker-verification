docker run \
     --user 0 \
     --volume="/etc/group:/etc/group:ro" \
     --volume="/etc/passwd:/etc/passwd:ro" \
     --volume="/etc/shadow:/etc/shadow:ro" \
     -v $PWD:/root/ -w /root/ \
     -v /var/run/docker.sock:/var/run/docker.sock \
     --network mobileid \
     -p 8888:8888 \
     shell-notebook jupyter notebook --allow-root 
