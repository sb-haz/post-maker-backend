# FROM tburrows13/moviepy
# FROM jonathangoorin/moviepy
FROM python:3.9.7
RUN pip install --upgrade pip

WORKDIR /post-maker-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

# ENV FLASK_ENV = development
CMD [ "python", "main.py" ]

# docker image build -t post-maker-app:latest .
# docker run -p 5000:5000  -d -t --name "post-maker-container" pm-app:latest