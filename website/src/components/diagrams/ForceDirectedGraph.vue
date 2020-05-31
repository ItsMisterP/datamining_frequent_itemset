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
            radius: 10,
            gravity: -10000,
            nodeClicked: false,
            containerClicked: false
        };
    },
    methods: {
        init() {
            let width = window.innerWidth;
            let height = window.innerHeight;
            var svg = d3
                .select("svg")
                .attr("viewBox", "0 0 " + width + " " + height);

            var radius = 15;
            var simulation = d3.forceSimulation().nodes(this.graph.nodes);
            var link_force = d3.forceLink(this.graph.links).id(function(d) {
                return d.id;
            });
            var charge_force = d3.forceManyBody().strength(this.gravity);
            var center_force = d3.forceCenter(width / 2, height / 2);
            simulation
                .force("charge_force", charge_force)
                .force("center_force", center_force)
                .force("links", link_force);
            //add tick instructions:
            simulation.on("tick", tickActions);
            var g = svg
                .append("g")
                .attr("class", "everything")
                .on("click", this.containerclicked);

            //draw lines for the links
            var link = g
                .append("g")
                .attr("class", "links")
                .selectAll("line")
                .data(this.graph.links)
                .enter()
                .append("line")
                .attr("stroke-width", 2)
                .style("stroke", function(d) {
                    return d.col;
                });
            //draw circles for the nodes
            var node = g
                .append("g")
                .attr("class", "nodes")
                .selectAll("circle")
                .data(this.graph.nodes)
                .enter()
                .append("g")
                .classed("circles", true);

            let circles = node
                .append("circle")
                .attr("r", radius)
                .attr("fill", function(d) {
                    return d.col;
                })
                .on("click", nodeclicked);

            node.append("text")
                .attr("dx", radius + 5)
                .attr("dy", ".35em")
                .attr("font-weight", "bold")
                .attr("fill", function(d) {
                    return d.col;
                })
                .text(function(d) {
                    return d.id;
                })
                .style("pointer-events", "none");
            //add drag capabilities
            var drag_handler = d3
                .drag()
                .on("start", drag_start)
                .on("drag", drag_drag)
                .on("end", drag_end);

            drag_handler(node);
            d3.selectAll("circle")
                .append("svg:title")
                .text(function(d) {
                    return "Item: " + d.id + "\n" + "support: " + d.support;
                });

            //add zoom capabilities
            var zoom_handler = d3.zoom().on("zoom", zoom_actions);
            zoom_handler(svg);

            function tickActions() {
                //update circle positions each tick of the simulation
                node.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });
                //update link positions
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
            function drag_start(d) {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }
            //make sure you can't drag the circle outside the box
            function drag_drag(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
            }
            function drag_end(d) {
                if (!d3.event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
            //Zoom functions
            function zoom_actions() {
                g.attr("transform", d3.event.transform);
            }
            let comp = this;
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

            function isNeighborLink(node, link, selectedNode) {
                if (
                    node.includes(link.target.id) &&
                    node.includes(link.source.id)
                ) {
                    return true;
                }
                return false;
            }

            function getNodeColor(node, neighbors) {
                if (neighbors.indexOf(node.id)) {
                    return node.level === 1 ? "blue" : node.col;
                }
                return node.level === 1 ? "red" : "gray";
            }
            function getTextColor(node, neighbors) {
                return neighbors.indexOf(node.id) ? "green" : node.col;
            }
            function getStrokeWidth(neighbor, link, selectedNode) {
                let value = 2;

                if (isNeighborLink(neighbor, link)) {
                    value = 10;
                }

                return value;
            }

            function nodeclicked(selectedNode) {
                this.nodeClicked = true;
                this.containerClicked = false;
                //console.log("node clicked");
                comp.$emit("nodeclicked", selectedNode);

                const neighbors = getNeighbors(selectedNode);
                //console.log(neighbors)
                circles.attr("fill", node => getNodeColor(node, neighbors));
                //textElements.attr("fill", node => getTextColor(node, neighbors));
                link.attr("stroke-width", link =>
                    getStrokeWidth(neighbors, link, selectedNode)
                );
            }
        },
        update() {
            d3.select(".everything").remove();
            this.init();
        },
        nodeclicked(selectedNode) {},
        containerclicked(d) {
        }
    }
};
</script>

<style scoped></style>
