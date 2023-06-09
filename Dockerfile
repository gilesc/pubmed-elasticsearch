FROM ubuntu:22.04

RUN apt update
RUN apt-get install -y python3.10 wget curl libxml2-dev
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install "elasticsearch==7.12.0"
RUN pip install "lxml"
RUN pip install tqdm

RUN curl --retry 10 -S -L -o /bin/tini "https://github.com/krallin/tini/releases/download/v0.19.0/tini-amd64"
RUN chmod +x /bin/tini

RUN mkdir /script
COPY src/wait-for-it.sh /script/
COPY src/update_pubmed.py /script/
COPY src/update_pubtator.py /script/
COPY src/daemon.sh /script/
COPY src/docker-entrypoint.sh /script/
RUN chmod +x /script/*

WORKDIR /script
ENTRYPOINT ["/bin/tini", "--", "/script/docker-entrypoint.sh"]
CMD ["daemon.sh"]
