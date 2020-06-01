<template>
    <div>
        <svg id="network"></svg>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";

export default {
    props: {
        graph: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            graphSetting: {
                radius: 10,
                clickedRadius: 25,
                strokeWidth: 2,
                clickedStrokeWidth: 10,
                textMargin: 5,
                gravity: -10000,
            },
            
            
            nodeClicked: false,
            containerClicked: false
        };
    },
    methods: {
        init() {
            let width = window.innerWidth;
            let height = window.innerHeight;

            // Den Graph hat dadurch immer die passenden Seitenverhältnisse und kann auch auf kleinen
            // Displays dargestellt werden
            var svg = d3
                .select("svg")
                .attr("viewBox", "0 0 " + width + " " + height)
                .on("click", containerclicked);

            // Initialisiere Kräfte und die Simulation
            var simulation = d3.forceSimulation().nodes(this.graph.nodes);
            var link_force = d3.forceLink(this.graph.links).id(function(d) {
                return d.id;
            });
            var charge_force = d3.forceManyBody().strength(this.graphSetting.gravity);
            var center_force = d3.forceCenter(width / 2, height / 2);
            simulation
                .force("charge_force", charge_force)
                .force("center_force", center_force)
                .force("links", link_force);
            
            // Füge die Tick-Methode zur Simulation hinzu -> Wird bei jedem Tick aufgerufen
            simulation.on("tick", tickActions);
            var g = svg
                .append("g")
                .attr("class", "everything");
                

            // Erstelle die Linien
            var link = g
                .append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(this.graph.links)
                .enter()
                .append("line")
                .attr("stroke-width", this.graphSetting.strokeWidth)
                .style("stroke", function(d) {
                    return d.col;
                });

            // Erstelle die Knotencontainer -> Jeder Container enthält den Knoten
            // und den Text -> einfacher die Knoten mit dem Text zu verschieben
            var node = g
                .append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(this.graph.nodes)
                .enter()
                .append("g")
                .classed("circles", true);

            // Erstelle die Knoten innerhalb eines Containers. Jeder Knoten besitzt einen
            // Radius, Farbe und eine on-Click Methode
            let circles = node
                .append("circle")
                .attr("r", this.graphSetting.radius)
                .attr("fill", function(d) {
                    return d.col;
                })
                .on("click", nodeclicked);

            // Füge den Text pro Container ein. Besitzt eine Farbe, einen Text, Größe usw. 
            // Wenn über den Text gehovered wird, wird der Mauszeiger nicht verändert
            node.append("text")
                .attr("dx", this.graphSetting.radius + this.graphSetting.textMargin)
                .attr("dy", ".35em")
                .attr("font-weight", "bold")
                .attr("fill", function(d) {
                    return d.col;
                })
                .text(function(d) {
                    return d.id;
                })
                .style("pointer-events", "none");

            // Ermöglicht das Ziehen eines Knotens und des gesamten Bildschirmes
            var drag_handler = d3
                .drag()
                .on("start", drag_start)
                .on("drag", drag_drag)
                .on("end", drag_end);


            // Ermöglicht das Zoomen im Diagramm
            var zoom_handler = d3.zoom().on("zoom", zoom_actions);
            zoom_handler(svg);

            // Setze Init-Zoom - https://stackoverflow.com/questions/16178366/d3-js-set-initial-zoom-level
            svg.call(zoom_handler.transform, d3.zoomIdentity.translate(width/2, height/2).scale(0.1));
            g.attr("transform","translate("+ width/2 +","+ height/2 +") scale(.1,.1)");

            // Diese Methode wird pro Tick und auf jedem Element aufgerufen. Jeder Knoten enthält Attribute, 
            // welche bei der Simulation geändert werden und angeben wo das Element neu positioniert werden
            // müssen
            function tickActions() {
                // Knoten updaten
                node.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });
                // Kanten updaten
                link.attr("x1", function(d) {
                    return d.source.x;
                })
                    .attr("y1", function(d) {
                        return d.source.y;
                    })
                    .attr("x2", function(d) {
                        return d.target.x;
                    })
                    .attr("y2", function(d) {
                        return d.target.y;
                    });
            }
            //Drag functions
            //d is the node
            // Die eigentliche Drag-Funktion. AlphaTarget sorgt für ein angenehmeres Gefühl beim
            // Ziehen. D ist der Knoten und wir updaten das Delta unseres ziehens innerhalb des Knotens
            function drag_start(d) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }

            // Stellt sicher, dass man nicht aus dem SVG raus kann.
            function drag_drag(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }

            //Drag functions
            //d is the node
            // Die eigentliche Drag-Funktion. AlphaTarget sorgt für ein angenehmeres Gefühl beim
            // Ziehen. D ist der Knoten und wir updaten das Delta auf Null
            function drag_end(d) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }

            // Zoom-Funktion
            function zoom_actions() {
                g.attr("transform", d3.event.transform);
            }

            let comp = this;

            // Sucht die Nachbarn eines Knotens. Herausforderung war, dass wir über zwei Kanten hinweg
            // die Nachbarn finden mussten, damit angezeigt wird, welche Knoten in Relation zu dem selektierten
            // Knoten ist. Daher der rekursive Aufruf innerhalb der Methode.
            function getNeighbors(node) {
                return comp.graph.links.reduce(
                    (neighbors, link) => {
                        if (link.target.id === node.id) {
                            neighbors.push(link.source.id);
                            if (link.source.type === "rule") {
                                let ruleNodes = getNeighbors(link.source);
                                //neighbors.push(ruleNodes)
                                neighbors = neighbors.concat(ruleNodes);
                            }
                        } else if (link.source.id === node.id) {
                            neighbors.push(link.target.id);
                            if (link.target.type === "rule") {
                                let ruleNodes = getNeighbors(link.target);
                                //neighbors.push(ruleNodes)
                                neighbors = neighbors.concat(ruleNodes);
                            }
                        }
                        return neighbors;
                    },
                    [node.id]
                );
            }

            // Eine Kante gehört zu einem Nachbarn, wenn beide Knoten teil der Nachbarn sind. Wird nur auf einen 
            // gerpüft, wird eine Kante zu viel innerhalb des Graphen als Nachbarkante markiert.
            function isNeighborLink(neighbors, link, selectedNode) {
                if (
                    neighbors.includes(link.target.id) &&
                    neighbors.includes(link.source.id)
                ) {
                    return true;
                }
                return false;
            }

            // Wenn der Knoten Teil der Nachbarn ist, dann gebe einen größeren Radius zurück
            function getNodeRadius(node, neighbors) {
                if (neighbors.includes(node.id)) {
                    return comp.graphSetting.clickedRadius;
                }
                return comp.graphSetting.radius;
            }

            // Wenn die Kante eine Nachbarschaftskante ist, dann gebe einen größeren Wert zurück
            function getStrokeWidth(neighbor, link, selectedNode) {
                let value = comp.graphSetting.strokeW;

                if (isNeighborLink(neighbor, link)) {
                    value = comp.graphSetting.clickedStrokeWidth;
                }

                return value;
            }

            // On-Click-Methode der Knoten
            function nodeclicked(selectedNode) {
                comp.nodeClicked = true;
                comp.containerClicked = false;
                // Sendet Signal an Parent, dass ein Knoten angeklickt wurde -> Diese aktualisiert die 
                // Tabelle, sodass nur die Regeln des Knotens angezeigt werden
                comp.$emit("nodeclicked", selectedNode);

                // Finde Nachbarn
                const neighbors = getNeighbors(selectedNode);

                // Highlighte alles, was zur Nachbarschaft gehört.
                circles.attr("r", node => getNodeRadius(node, neighbors));
                node.select("text").attr("dx", node => getNodeRadius(node, neighbors) 
                                                            + comp.graphSetting.textMargin);
                link.attr("stroke-width", link =>
                    getStrokeWidth(neighbors, link, selectedNode)
                );
            }

            // Die Differenzierung zwischen Knoten-Klick und nicht Knoten-Klick muss mit Hilfe einer Hilfs-
            // Variablen stattfinden. Mit ihr ist es Möglich zu prüfen, ob vorher ein Knoten gedrückt wurde.
            // Das geht, da das Knotenevent immer als erstes gefeuert wird.
            function containerclicked(d) {
                if(!comp.nodeClicked){
                    comp.containerClicked = true;
                    circles.attr("r", comp.graphSetting.radius);
                    node.select("text").attr("dx", comp.graphSetting.textMargin);
                    link.attr("stroke-width", comp.graphSetting.strokeWidth);
                }
                comp.nodeClicked = false;
            }
        },
        // Wenn sich Daten ändern, dann zeichne den Graphen neu
        // TODO: Richtiges Update durchführen.
        update() {
            d3.select(".everything").remove();
            this.init();
        },
        
    }
};
</script>

<style scoped></style>
