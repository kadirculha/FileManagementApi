FROM python:3.8
LABEL authors="ACULHA"
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /code
COPY ./ /code
CMD ["python3", "api.py"]

# docker rm -f get_corridors
# docker run -d -ti -v "PAth your Corridors File:app/Corridors" --name get_corridors -p 8888:8888 get_corridors
# docker rm -f get_corridors
# docker image rm -f get_corridors
# docker build -t get_corridors .

# docker save otel-comment2 > otel-comment2.tar

# docker load < otel-comment.tar
# docker run -d --restart always --name otel-comment -p 8008:8008 --env-file .env otel-comment2