<!-- $theme: default -->

# <center><b>Formation blockchain</b></center>
<center>Animée par: <b>Ladjimi Chiheb Eddine</b></center>
<center>Date: <b>14 - 15 Juillet 2018</b></center>

---

## À propos du formateur:

<img src="img/me.png" height="350"></img>

---
<!--
page_number: true
Formation blockchain
-->

## Plan de la formation

- Introduction
- Définition de la blockchain
- Bitcoin blockchain

	- Transaction, minage, colored coins, ...
	- Consommation des données
	- Les défauts et problèmes de Bitcoin

- Ethereum blokchain: Au delà de la blockchain de Bitcoin

	- Transaction, minage, smart contracts, ...
	- EVM, Dapps, blockchain 2.0, ...

---

- Nexus Blockchain: Implémentation éducative de la blockchain

	- Comment créer une blockchain from scratch ?
	- Comment réecrir la blockchain pour répondre à nos besoins ?
	- Et après ?

- Workshop

	- Créez votre propre implémentation de la blockchain !
	- Les pros & cons de vos implémentations

---

## Avant de commencer

- Qui êtes vous ?
- Avez-vous de l'expérience avec un ou plusieurs langages de programmation ?
- Que connaissez-vous de la blockchain ?
- Avez-vous déjà croisé des applications basées sur la technologie de la blockchain ?
- Avez-vous essayé d'utiliser la blockchain dans vos applications ? Avez-vous croiser des problèmes ?
- Quels sont vos objectifs à la fin de cette formation ?
- Autres questions avant de commencer la formation ?

---

# <center><b>Introduction</b></center>

Une (ou un) blockchain, ou chaîne de blocs, est une technologie de stockage et de transmission d'informations <b>sans organe de contrôle</b>. Techniquement, il s'agit d'une <b>base de données distribuée</b> dont les informations envoyées par les utilisateurs et <b>les liens internes à la base</b> sont <b>vérifiés et groupés à intervalles de temps réguliers en blocs</b>, <b>l'ensemble étant sécurisé par cryptographie</b>, et formant ainsi <b>une chaîne</b>. Par extension, <b>une chaîne de blocs est une base de données distribuée qui gère une liste d'enregistrements protégés contre la falsification ou la modification par les nœuds de stockage</b>. Une blockchain est donc un registre distribué et sécurisé de toutes les transactions effectuées depuis le démarrage du système réparti. [Source: wikipedia]

---

<center><img src="./img/Blockchain.png" height="500" width="200"></center>
<center>Représentation d’une chaîne de blocs. </center>

La chaîne principale (en noir) est composée de la plus longue suite de blocs après le bloc initial (vert). 
Les blocs orphelins sont représentés en violet.

---

### Des technologies qui ressemblent à la blockchain:

- Torrent: Distribuée mais n'est pas décentralisée
- Git: Distribuée mais n'est pas décentralisée
- Cloud storage: Distribuée mais pas décentralisée
- Zeronet: Décentalisée et distribuée
- etc ...

### Ce que la blockchain approte de nouveau: 

- Architecture décentralisée <b>et</b> distribuée
- Avec ou sans permissions
- <b>Confiance </b>

---

# <center>Bitcoin blockchain</center>

### La première implémentation de la blockchain

- Bitcoin

	- Monnaie (Digital Cash) sans organisation centrale et sans institution fiancière
	- Mécanisme de prévention contre la <b>Double Spending</b> (double dépense)
	- Une base de donnée décentralisée et distribuée

---

### Les avantages de cette implémentation

- Échanges directs entre utilisateurs (P2P)
- Frais de transactions beaucoup plus bas que les transactions monétaires traditionnelles
- Utilisable dans n'importe quel pays (contre la censure)
- Aucun ne peut contrôler votre argent seulement vous mêmes (techniquement: Celui qui possède la clé privée de l'adresse bitcoin)

---

### Comment le Bitcoin fonctionne

- Un bloc d'origine doit être crée (Genesis Block)
- Les utilisateurs échangent entre eux des jetons (Bitcoin) sous formes de transactions dans la blockchain de Bitcoin via les noeuds de Miners (mineurs full nodes) ou bien via des détenteurs de l'historique synchronisé de la blockchain de Bitcoin (light nodes)
- Entre temps, les Mineurs (Miners) cherchent de résoudre l'algorithme de preuve de travail proposé par Bitcoin (mécanisme de prévention de la double dépense) et le premier qui trouve la solution la propage dans le réseau.
- Cette solution est le Hash (le nom) du bloc trouvé et qui est constitué d'un ensemble de transaction des utilisateurs répendant à la taille du bloc déjà fixé par le logiciel de minage

--- 

- L'ensemble choisi des transactions seront soi confirmées ou non par les mineurs qui doivent tous trouver la même solution du hash du bloc pour ensuite valider ou non l'ensemble des transactions.
- Chaque mineur qui a trouvé le hash du bloc aura une récompense de la part du logiciel de minage (actuellement 12.5 btc et au début de bitcoin était 50 btc qui seront divisés sur 2 chaque 4 ans).
- La transaction déclinée ne sera pas inscrite dans la blockchain et les fonds resteront intactes et une transaction peut rester du temps sans être confirmée (problème de frais ou instabilité du réseau ou autres).
- Une transaction avec un nombre élevé de confirmations et une transaction plus sure comparant à une transaction avec un faible nombre de confirmations.
---

- Si un mineur A trouve une solution à un bloc en un instant `T` et un autre mineur B trouve la même solution en instant `T+x`. Dans ce cas, les mineurs qui ont reçu le hash du block de la part du mineur A vont essayer de résoudre le prochain bloc. S'il réussissent de trouver le prochain hash avant l'arrivée de l'information du hash trouvé par B alors la chaîne B sera rejettée et nommé `orphaned block` sinon si ceux qui ont miné en dessus de bloc du mineur B ont trouvé la solution du prochain block avant ceux qui ont miné en dessus du block trouvé par A, le block trouvé par A sera un `orphaned block`. Sinon, la compétition entre les blocs restera ouverte jusqu'à la défaite d'une chaîne contre une autre, ceci est appelé `orphaned chain` 
[Pour plus d'informations: https://www.blockchain.com/fr/btc/orphaned-blocks](https://www.blockchain.com/fr/btc/orphaned-blocks)

---

- Les mineurs peuvent trouver un hash différent pour un bloc (l'ensemble des transaction n'est pas le même ou autre contrainte) et là c'est aux mineurs de décider quel bloc choisir selon la propagation de l'information du hash trouvé entre les mineurs.
- Si un mineur triche et modifie les informations d'une ou plusieurs transaction(s), ce dernier doit refaire le calcul et modifier l'ensemble des blocs qui sont superposés à cet bloc (ceci demande énormément de calcul et dans le cas présent c'est irréalisable)
- La difficulté de résolution de l'algorithme du preuve de travail augmente chaque 2016 blocks et le hash du bloc trouvé doit être inférieur à `current_target` (formule: `difficulty = difficulty_1_target/current_target`) [[Plus d'informations](https://en.bitcoin.it/wiki/Difficulty)]

---

- Pour consommer les données enregistrées via la blockchain de Bitcoin:

	- On peut télécharger l'intégralité de la blockchain en utilisant un client de Bitcoin ([Bitcoin core (C++)](https://github.com/bitcoin/bitcoin) ou [btcd (Go)](https://github.com/btcsuite) ou [Bcoin (NodeJS)](https://github.com/bcoin-org/bcoin), etc..)
	- On peut utiliser des Light nodes tel [Electrum](https://electrum.org/#home), etc..
	- On peut aussi utiliser les APIs des explorateurs des blocs tel [Blockchain.info](https://www.blockchain.com/fr/explorer), [Blockcypher](https://live.blockcypher.com/), etc..

---

### Les problèmes de Bitcoin

- Scalability:
	- Limite de nombre de transactions par seconde (entre ~3.3 - ~7 transactions par secondes)
	- Taille de block 1MB (>~ 1MB avec Segwit et >> 1MB avec les sidechaines)
	- ~10 minutes entre chaque bloc
- Stockage:

	- Les mineurs et les noeuds doivent enregistrer l'intergalité de la blockchain (la taille des données prennent une forme exponontielle avec le temps)
	- Beaucoup de données (précisément dans les transactions) n'ont pas une grande utilité futuriste tel la nécissité d'inscrire les inputs de chaque transaction

---

