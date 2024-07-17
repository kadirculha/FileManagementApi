docker rm -f corridor
docker run -d -it -v ":/code/Corridors" --name corridor -p 8001:8001 corridor