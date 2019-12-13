FROM python:alpine

RUN pip install django && \
    mkdir olo

COPY . /olo

RUN chmod +x /olo/start.sh

WORKDIR /olo

EXPOSE 8000

CMD ["/olo/start.sh"]