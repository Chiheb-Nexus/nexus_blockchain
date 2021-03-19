FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/nexus_blockchain
WORKDIR /home/nexus_blockchain
ADD requirements.txt /home/nexus_blockchain/
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /home/nexus_blockchain/
