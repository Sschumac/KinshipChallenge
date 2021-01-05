FROM ubuntu:20.04
COPY ./app ./app
RUN apt update
RUN apt install -y pipenv
RUN cd app && \
pipenv install --system --deploy
CMD python3 ./app/index.py
EXPOSE 8099