
--Projet MiniAuditeur - Audit de surface d’exposition : Azure + Kali--

1. Mise en place du laboratoire d’audit
Dans le cadre de ce projet, nous avons mis en place un environnement complet permettant de réaliser un audit réseau et web en conditions réelles. La machine cible utilisée est une machine virtuelle Ubuntu hébergée sur Microsoft Azure. Cette VM a été configurée comme un véritable serveur accessible depuis Internet, avec une adresse IP publique et des ports ouverts pour permettre les tests d’intrusion.

2. Configuration de la machine cible (Ubuntu Azure)
Sur la VM Ubuntu, nous avons installé le serveur web Apache2, afin de disposer d’un service HTTP fonctionnel. Pour activer la couche HTTPS, nous avons généré un certificat SSL auto signé directement sur la machine Ubuntu. Ce certificat n’étant pas émis par une autorité de certification reconnue, il est considéré comme non valide, ce qui a été confirmé lors des tests TLS.
La VM Ubuntu exposait les ports suivants :
•	22 : SSH
•	80 : HTTP
•	443 : HTTPS
Ces ports ont été volontairement laissés ouverts pour permettre l’analyse complète de la surface d’exposition du serveur.

3. Développement de l’outil MiniAuditeur
Le développement de l’outil a été réalisé sur ma machine Windows, en utilisant Visual Studio Code comme environnement de programmation. Le projet est entièrement codé en Python, sous forme de modules spécialisés :
•	Scan de ports
•	Analyse des en têtes HTTP
•	Analyse TLS / SSL
•	Génération automatique d’un rapport Markdown
Une fois le code finalisé, nous avons créé un dépôt GitHub afin de versionner le projet et de le rendre accessible depuis n’importe quelle machine.

4. Mise en place de la machine d’attaque (Kali Linux)
La machine utilisée pour réaliser les tests d’intrusion est une VM Kali Linux, configurée comme poste d’audit. Depuis Kali, nous avons cloné le dépôt GitHub contenant le code Python :
Code
git clone https://github.com/montchonabil-collab/miniauditeur.git
Cela nous a permis d’exécuter l’outil directement depuis Kali, comme le ferait un véritable pentester.

5. Réalisation des tests d’audit
Une fois l’outil exécuté depuis Kali, plusieurs tests ont été réalisés sur la VM Ubuntu Azure :
Scan de ports :

python3 cli.py --target 40.66.52.60 --ports 1-100 --urls http://40.66.52.60 --tls 40.66.52.60 --report

Le module de scan a permis d’identifier les ports ouverts sur la machine cible. Les résultats ont confirmé la présence des ports 22, 80 et 443 en écoute.
Analyse des en têtes HTTP
Le module HTTP a interrogé le serveur Apache pour récupérer les en têtes renvoyés. Cette analyse permet d’évaluer le niveau de sécurité du serveur web (présence ou absence de headers critiques).
Analyse SSL / TLS
Le module TLS a inspecté le certificat du serveur HTTPS. Le résultat a montré que :
•	le certificat était auto signé,
•	il était émis par la VM elle même,
•	il n’était pas reconnu comme valide par les navigateurs ou outils de sécurité.
Ce comportement est normal pour un certificat auto signé, mais constitue une faiblesse dans un contexte de production.

6. Génération du rapport d’audit
L’outil MiniAuditeur produit deux types de résultats :
    1. Un affichage en texte brut dans le terminal Kali
Chaque test affiche immédiatement ses résultats dans la console, permettant une lecture rapide.
    2. Un fichier de rapport automatique au format Markdown (.md)
Ce fichier contient :
•	les ports détectés,
•	les en têtes HTTP analysés,
•	les informations TLS,
•	une synthèse globale de l’audit.
Ce rapport constitue un livrable professionnel, exploitable pour une soutenance ou un audit réel.

7. Conclusion générale
Ce projet a permis de mettre en place un laboratoire complet d’audit réseau et web, incluant :
•	une machine cible Azure configurée comme un vrai serveur,
•	une machine d’attaque Kali Linux,
•	un outil Python modulaire et fonctionnel,
•	un dépôt GitHub pour la gestion du code,
•	des tests d’intrusion réalisés en conditions réelles,
•	un rapport automatique documentant les résultats.

MiniAuditeur démontre une approche professionnelle de l’audit de surface d’exposition, combinant développement, cloud, sécurité web, réseau et bonnes pratiques DevSecOps.

