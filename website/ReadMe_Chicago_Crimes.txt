Readme-Datei  zu eingesetzten Visualisierungstechniken undzu Quellen (Daten, Bibliotheken, abgewandelte Code-Beispiele)

Benutzung: 
Die Webseite ist online einsehbar unter dem folgendem Link:
http://94.130.204.236:12000/#/dashboard

Oder die Webseite wird mit einem NodeJS-Server und Python-Server deployed:
- Dazu muss NodeJS, NPM  und Python3 installiert sein
- Vue installieren mit " npm install -g @vue/cli "
- Im Rootverzeichnis in einer Konsole: " npm install " ausführen
- Danach mit: " npm run serve ", um die Webseite in einem NodeJS-Server zu starten
- Neue Konsole öffnen und in das Verzeichnis /src/assets wechseln
- Mit dem Kommando: " python start_webserver.py " den Webserver starten. 
	Bitte das Skript verwenden, da zum einen der Port richtig eingestellt ist und zum anderen der Webserver bestimmte Einstellungen besitzt
- Nun ist die Webseite unter localhost:8080 erreichbar. 
	Falls die Webseite beim Deployment schon geöffnet wurde, einmal refreshen, um die Daten vom Pythonserver zu erhalten.


Visualisierungstechniken:
Alle Visualisierungsmethoden basieren auf folgenden Ansatz:
	Overview -> Filter -> Detail
	
Heatmap mit einem Tortendiagramm und einer Tabelle.
Force-Directed-Graph mit einer Tabelle und einer Filterfunktion.
Parallel Koordinaten Diagramm mit einer Tabelle.


Referenzen:
Data mining / Association Pattern Mining:
Master Seminar von Robin Buchta & Philip Ohm

Vue JS: https://vuejs.org/
Vue Material Dashboard: https://www.creative-tim.com/product/vue-material-dashboard
Components: https://vuematerial.io/components/
Heatmap: http://bl.ocks.org/cjhin/27e01c636dcc0bfa256c7a225971354d
Geojson processing: https://www.npmjs.com/package/vue-d3-geo
District geo data: https://data.cityofchicago.org/Public-Safety/Boundaries-Police-Districts-current-/fthy-xz3r
Heatmap gradient legend:  https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient
Pie chart: Bachelor Thesis by Philip Ohm
Force directed graph: https://bl.ocks.org/puzzler10/4438752bb93f45dc5ad5214efaa12e4a
Force directed graph Initial zoom level: https://stackoverflow.com/questions/16178366/d3-js-set-initial-zoom-level
Force directed graph Clickable nodes: https://medium.com/ninjaconcept/interactive-dynamic-force-directed-graphs-with-d3-da720c6d7811
Parallel Coordinates: https://syntagmatic.github.io/parallel-coordinates/
Parallel Coordinates adapted for v5: https://github.com/BigFatDog/parcoords-es
Parallel Coordinates Reset Button: http://bl.ocks.org/sc28/afa69162dc61833dc19fec7f0094f01a