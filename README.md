# Projet de Blockchain
Projet dans le cadre du cours de Blockchain 2022-2023, dont la page du cours est disponible [ici](https://www.lri.fr/~conchon/blockchain/).

# Requis
Python 3.10 est nécessaire pour lancer le projet.

# Comment tester le projet
## Etape 1: Création du réseau
* Pour le premier mineur (celui qui mine le bloc genesis):
```bash
python miner.py localhost port
```
port étant le port que le miner utilisera pour accepter les connexions.

* Pour un miner quelconque:
```bash
python miner.py localhost port_o localhost port_d
```
avec port_o l'adresse du mineur, et port_d le port (d'un autre mineur) auquel il veut se connecter

* Pour un wallet:
```bash
python wallet.py localhost port_o port_d
```
avec port_o l'adresse du wallet, et port_d le port (d'un mineur) auquel il veut se connecter

## Etape 2: Envoi de transactions et Proof of work
* Un wallet envoie des fonds à l'aide de la commande suivante:
```
/transac adr_destination montant
```
adr_destination étant l'adresse d'un wallet et montant, la quantité que le wallet souhaite envoyer.
* Un mineur, lorsqu'il le souhaite, exécute la preuve de travail en saisissant:
```
do_pow
```
* Lorsqu'un mineur a réussit la preuve de travail, il diffuse le nouveau bloc à travers le réseau.

## Vérifier qu'une transaction existe
Un mineur peut voir si une transaction est dans la blockchain en saisissant la commande
```
/check origine destination montant
```
avec origine et destination, les adresses d'origine et destination de la transaction, et montant, la quantité de token transféré

## Token disponible pour un wallet
Un wallet peut regarder la quantité de token qu'il possède avec la commande
```
/balance
```
