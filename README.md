# nexus_blockchain
A tiny implementation of blockchain technology using a custom proof of work called "Proof of Nexus"

# Installation

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
- Then you have a list of a files try them all if you want :-)

# PS:

This project still in eraly phase, only some API's are implemented.
In the next commit i'll add some more API's and some views :-)
