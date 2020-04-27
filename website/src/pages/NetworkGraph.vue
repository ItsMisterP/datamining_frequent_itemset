<template>
    <div>
        <md-layout>
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <div id="graphDiv"></div>
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Filter</h4>
                    </md-card-header>
                    <md-card-content>
                        <label for="networkminsup">Min-Sup for Rules:</label
                        ><br />
                        <input
                            id="networkminsup"
                            @change="update"
                            type="range"
                            v-model.number="minsup"
                            min="0"
                            max="0.3"
                            step="0.001"
                        />
                        {{ minsup }}
                        <br />
                        <label for="networkminsup">Kluc for Rules:</label><br />
                        <input
                            id="networkminsup"
                            @change="update"
                            type="range"
                            v-model.number="kluc"
                            min="0"
                            max="1"
                            step="0.01"
                        />
                        {{ kluc }}
                        <br />
                        <label for="networkminsup">Imb-Ratio for Rules:</label
                        ><br />
                        <input
                            id="networkminsup"
                            @change="update"
                            type="range"
                            v-model.number="imb"
                            min="0"
                            max="1"
                            step="0.01"
                        />
                        {{ imb }}
                        <br />
                        <label for="networkminsup">Gravity for Rules:</label
                        ><br />
                        <input
                            id="networkminsup"
                            @change="update"
                            type="range"
                            v-model.number="gravity"
                            min="-50000"
                            max="0"
                            step="1000"
                        />
                        {{ gravity }}
                        <br />
                        <md-checkbox :change="update" v-model="showItemsets"
                            >Show Itemsets</md-checkbox
                        >
                    </md-card-content>
                </md-card>
            </div>
        </md-layout>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";

export default {
    watch: {
        showItemsets: function() {
            this.update();
        }
    },
    data() {
        return {
            context: Object,
            width: 500,
            height: 500,
            items: [],
            frame: {
                canvas: Object,
                context: Object,
                width: 0,
                height: 0
            },
            simulation: Object,
            graph: {
                nodes: [],
                links: []
            },
            transform: Object,
            radius: 10,
            minsup: 0.005,
            kluc: 0.5,
            imb: 0.1,
            gravity: -10000,
            showItemsets: false
        };
    },
    mounted() {
        this.prepareData();
        this.init();
    },
    methods: {
        update() {
            d3.select("canvas").remove();
            this.graph.nodes = [];
            this.graph.links = [];
            this.prepareData();
            this.init();
        },
        prepareData() {
            let rules = require("../assets/json/association_rules.json");

            let filteredRules = rules.filter(item => {
                return item.support > this.minsup && item.kluc > this.kluc;
            });

            if (!this.showItemsets) {
                filteredRules.forEach(element => {
                    let value = 1000.0 * parseFloat(element.support);

                    this.graph.nodes.push({
                        id:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        type: "rule",
                        col: "#FF6B66",
                        radius: this.radius + value
                    });

                    let inputs = element.antecedents;
                    inputs.forEach(input => {
                        if (
                            this.graph.nodes.filter(node => node.id == input)
                                .length == 0
                        ) {
                            this.graph.nodes.push({
                                id: input,
                                col: "green",
                                radius: this.radius
                            });
                        }

                        this.graph.links.push({
                            source: input,
                            target:
                                "{" +
                                element.antecedents.join(",") +
                                "}->{" +
                                element.consequents.join(",") +
                                "}",
                            col: "blue"
                        });
                    });

                    let outputs = element.consequents;
                    outputs.forEach(output => {
                        if (
                            this.graph.nodes.filter(node => node.id == output)
                                .length == 0
                        ) {
                            this.graph.nodes.push({
                                id: output,
                                col: "green",
                                val: 2,
                                radius: this.radius
                            });
                        }

                        this.graph.links.push({
                            source:
                                "{" +
                                element.antecedents.join(",") +
                                "}->{" +
                                element.consequents.join(",") +
                                "}",
                            target: output,
                            col: "black"
                        });
                    });
                });
            } else {
                filteredRules.forEach(element => {
                    let value = 1000.0 * parseFloat(element.support);
                    this.graph.nodes.push({
                        id:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        type: "rule",
                        col: "#FF6B66",
                        radius: value
                    });

                    if (
                        this.graph.nodes.filter(
                            node =>
                                node.id ==
                                "{" + element.antecedents.join(",") + "}"
                        ).length == 0
                    ) {
                        let value2 = 1000.0 * parseFloat(element.as);
                        this.graph.nodes.push({
                            id: "{" + element.antecedents.join(",") + "}",
                            col: "green",
                            val: 2,
                            radius: value2
                        });
                    }
                    this.graph.links.push({
                        source: "{" + element.antecedents.join(",") + "}",
                        target:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        col: "blue"
                    });

                    if (
                        this.graph.nodes.filter(
                            node =>
                                node.id ==
                                "{" + element.consequents.join(",") + "}"
                        ).length == 0
                    ) {
                        let value3 = 1000.0 * parseFloat(element.as);
                        this.graph.nodes.push({
                            id: "{" + element.consequents.join(",") + "}",
                            col: "green",
                            val: 2,
                            radius: value3
                        });
                    }
                    this.graph.links.push({
                        source: "{" + element.consequents.join(",") + "}",
                        target:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        col: "black"
                    });
                });
            }
        },
        init() {
            var height = window.innerHeight;
            var graphWidth = window.innerWidth;

            var graphCanvas = d3
                .select("#graphDiv")
                .append("canvas")
                .attr("width", graphWidth + "px")
                .attr("height", height + "px")
                .node();

            var context = graphCanvas.getContext("2d");

            var div = d3
                .select("body")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);

            let gravity = this.gravity;

            var simulation = d3
                .forceSimulation()
                .force("center", d3.forceCenter(graphWidth / 2, height / 2))
                .force("x", d3.forceX(graphWidth / 2).strength(0.1))
                .force("y", d3.forceY(height / 2).strength(0.1))
                .force("charge", d3.forceManyBody().strength(gravity))
                .force(
                    "link",
                    d3
                        .forceLink()
                        .strength(1)
                        .id(function(d) {
                            return d.id;
                        })
                )
                .alphaTarget(0)
                .alphaDecay(0.05);

            var transform = d3.zoomIdentity;

            let data = this.graph;

            initGraph(data);

            function initGraph(tempData) {
                function zoomed() {
                    transform = d3.event.transform;
                    simulationUpdate();
                }

                d3.select(graphCanvas)
                    .call(
                        d3
                            .drag()
                            .subject(dragsubject)
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended)
                    )
                    .call(
                        d3
                            .zoom()
                            .scaleExtent([1 / 10, 8])
                            .on("zoom", zoomed)
                    );

                function dragsubject() {
                    var i,
                        x = transform.invertX(d3.event.x),
                        y = transform.invertY(d3.event.y),
                        dx,
                        dy;
                    for (i = tempData.nodes.length - 1; i >= 0; --i) {
                        let node = tempData.nodes[i];
                        dx = x - node.x;
                        dy = y - node.y;

                        if (dx * dx + dy * dy < node.radius * node.radius) {
                            node.x = transform.applyX(node.x);
                            node.y = transform.applyY(node.y);

                            return node;
                        }
                    }
                }

                function dragstarted() {
                    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                    d3.event.subject.fx = transform.invertX(d3.event.x);
                    d3.event.subject.fy = transform.invertY(d3.event.y);
                }

                function dragged() {
                    d3.event.subject.fx = transform.invertX(d3.event.x);
                    d3.event.subject.fy = transform.invertY(d3.event.y);
                }

                function dragended() {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d3.event.subject.fx = null;
                    d3.event.subject.fy = null;
                }

                simulation.nodes(tempData.nodes).on("tick", simulationUpdate);

                simulation.force("link").links(tempData.links);

                function render() {}

                function simulationUpdate() {
                    context.save();

                    context.clearRect(0, 0, graphWidth, height);
                    context.translate(transform.x, transform.y);
                    context.scale(transform.k, transform.k);

                    tempData.links.forEach(function(d) {
                        context.beginPath();
                        context.moveTo(d.source.x , d.source.y );
                        context.lineTo(d.target.x, d.target.y);
                        context.strokeStyle = d.col;
                        context.stroke();
                    });

                    // Draw the nodes
                    tempData.nodes.forEach(function(d, i) {
                        context.beginPath();
                        context.arc(d.x, d.y, d.radius, 0, 2 * Math.PI, true);
                        context.fillStyle = d.col;
                        context.fill();
                        context.fillText(d.id, d.x + d.radius+2, d.y + 3);
                    });

                    context.restore();
                }
            }
        }
    }
};
</script>
<style scoped>
.edge {
    stroke: white;
    stroke-width: 1;
}
.graphSVG {
    background-color: black;
}

div.container {
    width: 100%;
    border: 1px solid gray;
}
div.tooltip {
    position: absolute;
    text-align: center;
    width: 180px;
    padding: 2px;
    font: 12px sans-serif;
    background: lightsteelblue;
    border: 0px;
    border-radius: 8px;
    pointer-events: none;
}
input {
    width: 50%;
}
</style>
