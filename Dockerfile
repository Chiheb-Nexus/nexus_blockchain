FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/nexus_blockchain
WORKDIR /home/nexus_blockchain
ADD requirements.txt /home/nexus_blockchain/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /home/nexus_blockchain/
