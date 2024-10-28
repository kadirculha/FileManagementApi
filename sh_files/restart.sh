docker rm -f corridor
#docker run -d -it -v ":/code/Corridors" --name corridor -p 8080:8080 corridor
docker run -d -it -v "/home/ubuntu/Volume/Corridors:/code/Corridors" --name corridor -p 8080:8080 corridor

# "C:\Users\apoks\OneDrive\Masaüstü\AllDataFromUbuntu\work\AiThinks\Volume\Corridors"