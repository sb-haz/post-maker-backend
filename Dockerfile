# Dockerfile, Image, Container
FROM jonathangoorin/moviepy

WORKDIR /post-maker

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]