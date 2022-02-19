# Dockerfile, Image, Container
FROM jonathangoorin/moviepy

WORKDIR /post-maker

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]