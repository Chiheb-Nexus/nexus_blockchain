# Nexus Blockchain

[![CircleCI](https://circleci.com/gh/Chiheb-Nexus/nexus_blockchain/tree/master.svg?style=svg)](https://circleci.com/gh/Chiheb-Nexus/nexus_blockchain/tree/master)

A tiny implementation of blockchain technology using a custom proof of work called "Proof of Nexus"

## Installation

- Install `virtualenv` for `Python3` then clone and install the project


```bash
$> sudo pip install virtualenv
$> cd ~
$> virtualenv --python=`which python3` nexus_blockchain
$> cd nexus_blockchain/bin
$> source activate
$> cd ..
$> git clone https://github.com/Chiheb-Nexus/nexus_blockchain
$> cd nexus_blockchain
$> pip install -r requirements.txt
$> python manage.py makemigrations
$> python manage.py migrate
$> python manage.py createsuperuser
$> python manage.py runserver
```

- In a second terminal, activate the `virtualenv` then go to `~/YOUR_VENV_PATH/nexus_blockchain/interaction`

## DEMO

```bash
$> python create_wallet.py 
-> [27/06/2018 20:47:24] INFO: Wallet created - PATH: /home/chiheb/nexus_blockchain/nexus_blockchain/interaction/keystore/keys
$> python mining.py 
{"height":0,"transactions":[],"previous_hash":null,"timestamp":1530128945.550915,"data":"Genesis Block!","block_hash":"ff1099d5743ca5c21df440d9f3d2c90aec603aea46889797a9aa7899d21a7f54","merkle":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}
-> [27/06/2018 20:49:06] INFO: Trying to find new work ...
^C
Quit [q/Q] else Continue: q

$> python create_transaction.py 
-> [27/06/2018 21:08:49] INFO: Sending Transaction:
{"amount": 5, "to": "0x0000000000000000000000000000000000000000", "from": "0xE0179D4DA5b16443C18450f35e46B2a716ae8f74", "fees": 0.0001, "data": "0x", "timestamp": 1530130129.167453, "signature": "0xa998b1555fd5c9e4eb3872f36edc587a2406bdaf98044957bd0a9675667d8a3823886ae5e3f9701a3b0d81d190a2c13cd4641f88984753ec5f37e6c866c2a1731b"}

-> [27/06/2018 21:08:49] INFO: Server response: {"signature":true,"status":200,"tx_hash":"3aabcbf8e7f12a10eb4474b6ecdd35081b098da54815bb81cf8e146dfb4805dc"}
```

- Then you have a list of a files try them all if you want :-)

## Demo using Docker:

Simply install docker and docker-compose then:

```bash
$> sudo su # Pass to root user
$> cd docker_interaction
$> ./run_docker.sh # In one terminal
$> ./run_docker_bash.sh # In a second terminal
# In the second terminal within docker
root@[container_id]:/home/nexus_blockchain# cd interaction
root@[container_id]:/home/nexus_blockchain# python mining.py
```

## Screenshots

![block](./screenshots/block.png  "block")

![address](./screenshots/address.png  "address")

# PS:

- This project still in eraly phase, only some API's are implemented.
In the next commit i'll add some more API's and some views :-)

- This project is for education purposes only and is not meant for production
