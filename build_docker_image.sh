# in macos, make sure you start the docker.app before running this command.
export PUID=`id -u $USER`
export PGID=`id -g $USER`

docker build --no-cache \
    -t azure_data_api_server:1.0 \
    --build-arg PUID=$PUID \
    --build-arg PGID=$PGID \
    --build-arg USER=$USER \
    -f Dockerfile.dev .
