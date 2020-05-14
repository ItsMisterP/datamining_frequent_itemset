<template>
    <div>
        <div class="md-layout">
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
            >
                <svg id="network"></svg>
            </div>
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-50 md-size-50"
            >
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
                            min="0.00001"
                            max="0.3"
                            step="0.00001"
                        />
                        {{ minsup }}
                        <br />
                        <label for="klucmin">Minimum Kluc for Rules:</label
                        ><br />
                        <input
                            id="klucmin"
                            @change="update"
                            type="range"
                            v-model.number="klucMin"
                            min="0.0"
                            max="1"
                            step="0.01"
                        />
                        {{ klucMin }}
                        <br />
                        <label for="klucmax">Maximum Kluc for Rules:</label
                        ><br />
                        <input
                            id="klucmax"
                            @change="update"
                            type="range"
                            v-model.number="klucMax"
                            min="0.0"
                            max="1"
                            step="0.01"
                        />
                        {{ klucMax }}
                        <br />
                        <label for="imbratio">Imb-Ratio for Rules:</label>
                        <br />
                        <input
                            id="imbratio"
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
            <div
                class="md-layout-item md-medium-size-100 md-xsmall-size-50 md-size-50"
            >
                <md-card>
                    <md-card-header data-background-color="gray">
                        <h4 class="title">Association Rules</h4>
                    </md-card-header>
                    <md-card-content>
                        <md-table
                            v-model="tableRules"
                            md-sort="support"
                            md-sort-order="desc"
                            md-card
                            md-fixed-header
                        >
                            <md-table-empty-state
                                md-label="No Rules found"
                                :md-description="`No rules for the parameters`"
                            >
                            </md-table-empty-state>

                            <md-table-row
                                slot="md-table-row"
                                slot-scope="{ item }"
                            >
                                <md-table-cell
                                    md-label="Support"
                                    md-sort-by="support"
                                    md-numeric
                                >
                                    {{ item.support }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Antecedents"
                                    md-sort-by="antecedents"
                                >
                                    {{ item.antecedents }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Consequents"
                                    md-sort-by="consequents"
                                >
                                    {{ item.consequents }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Confidence"
                                    md-sort-by="confidence"
                                >
                                    {{ item.confidence }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Kluc"
                                    md-sort-by="kluc"
                                >
                                    {{ item.kluc }}
                                </md-table-cell>
                                <md-table-cell
                                    md-label="Imbalance Ratio"
                                    md-sort-by="imbratio"
                                >
                                    {{ item.imbratio }}
                                </md-table-cell>
                            </md-table-row>
                        </md-table>
                    </md-card-content>
                </md-card>
            </div>
        </div>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";
import { globalStore } from "../main";

export default {
    watch: {
        showItemsets: function() {
            this.update();
        }
    },
    data() {
        return {
            graph: {
                nodes: [],
                links: []
            },
            radius: 10,
            minsup: 0.00001,
            klucMin: 0.0,
            klucMax: 1,
            imb: 0,
            gravity: -10000,
            showItemsets: false,
            filteredRules: [],
            tableRules: [],
            graphCanvas: Object
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        fetchData() {
            let graph = this;
            d3.json(this.getURL("json/association_rules.json")).then(function(
                data
            ) {
                graph.rules = data;
                graph.prepareData();
                graph.init();
            });
        },
        update() {
            d3.select(".everything").remove();
            this.graph.nodes = [];
            this.graph.links = [];
            this.prepareData();
            this.init();
        },
        prepareData() {
            let rules = this.rules;
            this.filteredRules = rules.filter(item => {
                return (
                    item.support > this.minsup &&
                    item.kluc >= this.klucMin &&
                    item.kluc < this.klucMax &&
                    item.imbratio >= this.imb
                );
            });
            this.tableRules = this.filteredRules;

            if (!this.showItemsets) {
                this.filteredRules.forEach(element => {
                    let value = 1;

                    this.graph.nodes.push({
                        id:
                            "{" +
                            element.antecedents.join(",") +
                            "}->{" +
                            element.consequents.join(",") +
                            "}",
                        type: "rule",
                        col: "#FF6B66",
                        radius: this.radius + value,
                        support: element.support
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
                this.filteredRules.forEach(element => {
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

            var g = svg.append("g").attr("class", "everything");

            //svg.on("click", this.containerclicked);

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
                .on("click", this.nodeclicked);

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
        },
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        containerclicked(d) {
            console.log("tick");
            this.tableRules = this.filteredRules;
        },
        nodeclicked(d) {
            this.tableRules = this.filteredRules;

            this.tableRules = this.filteredRules.filter(item => {
                return (
                    item.antecedents.includes(d.id) ||
                    item.consequents.includes(d.id) ||
                    (
                        "{" +
                        item.antecedents.join(",") +
                        "}->{" +
                        item.consequents.join(",") +
                        "}"
                    ).includes(d.id)
                );
            });
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
