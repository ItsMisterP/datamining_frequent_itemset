Titel: 
	Chicago Crimes - Association Rule / Frequent Itemset Mining 

Teammitglieder:
	Jannik Badenhob
	Robin Buchta
	Philip Ohm

Visualisierungstechniken:
	Alle Visualisierungsmethoden basieren auf folgenden Ansatz:
		Overview -> Filter -> Detail
	Zielgruppe: Leute mich Fachwissen
	
	1.) Dashboard: Heatmap (in Kartenformat) mit einem Tortendiagramm und einer Tabelle.
	2.) Association Rules - Network: Force-Directed-Graph mit einer Tabelle und einer Filterfunktion.
	3.) Association Rules - Table: Parallel Koordinaten Diagramm mit einer Tabelle.

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
		- Nun ist die Webseite unter http://localhost:8080 erreichbar. 
			Falls die Webseite beim Deployment schon geöffnet wurde, einmal refreshen, um die Daten vom Pythonserver zu erhalten.
Benutzung (Webseite):
Webseite besteht aus 4 Views:
	1.) Dashboard:
		- Zeigt die Verbrechensaufkommen pro Distrikt an.
		- Wähle ein Distrikt auf der Heatmap, um weitere Informationen zu erhalten.
		- Tortendiagramm zeigt Werte, Attribute über Dropdown auswählbar, Tortenstückauswählbar - Hightlight in Tabelle.
		- Tabelle aktualisiert sich. 
		- Tabelle zeigt die Werte zugehörig der Farbe an. 
		- Tabelle zeigt die Werte absteigend sortiert an.
	2.) Association Rules - Network:
		- Zeigt die einzelnen Regeln an, welche durch das Preprocessing erstellt wurden.
		- Rote Knoten sind die Regeln, grüne sind die Items, welche innerhalb der Regel verwendet werden.
		- Tabelle unterhalb zeigt alle selektierten Regeln an.
		- Klick auf einen Knoten -> Alle anderen Knoten, welche mit dem angeklickten Knoten in Beziehung stehen, werden gehighlighted und
		  die Tabelle wird akutalisiert.
		- Klick außerhalb eines Knotens -> Deselektierung (kann einen kleinen Moment dauern, da die Tabellenaktualisierung teuer ist).
		- Filter aufklappbar, wodurch Metrikparameter gesetzt werden können.
		- Die Tabelle kann nach den Werten ab/ aufsteigend sortiert werden.
		- Zoom möglich. (Scoll in/out während Mauszeiger innerhalb des Netzwerkes)
		- Verschieben des Netwerkes möglich. (Mausklick und ziehen)
		- Knoten sind einzeln nicht verschiebbar.
	3.) Association Rules - Table:
		- Parallel Koordinaten Diagramm zeigt die Association Rules an mit ihren einzelnen Metik-Werten.
		- Jede Säule ist eine Metik und die Linien sind die Regeln. 
		- Die Linien haben einen Farbverlauf, um diese besser zu unterscheiden (Metrik: Confidence-Werte sind zuständig).
		- Die Säulen sind durch Anklicken und bewegen zu verschieben.
		- Auf einer Säule kann ein Intervall ausgewählt werden (Mausklick und ziehen). (Mehere Säulen gleichzeitig möglich)
		- Reset Button hebt die Markierung auf - nicht das verschieben der Säulen.
		- Tabelle zeigt die ausgewählten Regeln an.
		- Die Tabelle kann nach den Werten ab/ aufsteigend sortiert werden.
	4.) Information:
		- Infomationen zum Projekt (Mitglieder, Referenzen, Daten).
	

Referenzen:
	- Data mining / Association Pattern Mining:
	- Master Seminar von Robin Buchta & Philip Ohm

	- Vue JS: https://vuejs.org/
	- Vue Material Dashboard: https://www.creative-tim.com/product/vue-material-dashboard
	- Components: https://vuematerial.io/components/
	- Heatmap: http://bl.ocks.org/cjhin/27e01c636dcc0bfa256c7a225971354d
	- Geojson processing: https://www.npmjs.com/package/vue-d3-geo
	- District geo data: https://data.cityofchicago.org/Public-Safety/Boundaries-Police-Districts-current-/fthy-xz3r
	- Heatmap gradient legend:  https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient
	- Pie chart: Bachelor Thesis by Philip Ohm
	- Force directed graph: https://bl.ocks.org/puzzler10/4438752bb93f45dc5ad5214efaa12e4a
	- Force directed graph Initial zoom level: https://stackoverflow.com/questions/16178366/d3-js-set-initial-zoom-level
	- Force directed graph Clickable nodes: https://medium.com/ninjaconcept/interactive-dynamic-force-directed-graphs-with-d3-da720c6d7811
	- Parallel Coordinates: https://syntagmatic.github.io/parallel-coordinates/
	- Parallel Coordinates adapted for v5: https://github.com/BigFatDog/parcoords-es
	- Parallel Coordinates Reset Button: http://bl.ocks.org/sc28/afa69162dc61833dc19fec7f0094f01a


Speicherorte der Visualisierungstechniken (innerhalb des Source-Codes):
	- /src/pages/Dashboard.vue
	- /src/pages/NetworkGraph.vue
	- /src/pages/ParcoordsTable.vue
	- /src/pages/Information.vue

	- /src/components/diagrams/ForceDirectedGraph.vue
	- /src/components/diagrams/HeatMap.vue
	- /src/components/diagrams/PieChart.vue