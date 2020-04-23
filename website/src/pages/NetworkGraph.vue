<template>
    <div>
        <canvas width="960" height="600"></canvas>
    </div>
</template>
<script>
import * as d3 from "d3";
import { scaleLinear, scaleBand } from "d3-scale";
import { max, min } from "d3-array";
import { selectAll } from "d3-selection";

export default {
    data() {
        return {
            context: Object,
            width,
            height
        };
    },
    mounted() {
        this.init();
    },
    methods: {
        init() {
            var canvas = document.querySelector("canvas");
            this.context = canvas.getContext("2d");
            this.width = canvas.width;
            this.height = canvas.height;

            var simulation = d3
                .forceSimulation()
                .force(
                    "link",
                    d3.forceLink().id(function(d) {
                        return d.id;
                    })
                )
                .force("charge", d3.forceManyBody())
                .force(
                    "center",
                    d3.forceCenter(this.width / 2, this.height / 2)
                );

            let items = require("@/assets/json/test.json");
            console.log(items);

            simulation.nodes(items.nodes).on("tick", this.ticked);
        },
        ticked() {
            let context = this.context;

            context.clearRect(0, 0, this.width, this.height);

            context.beginPath();
            graph.links.forEach(drawLink);
            context.strokeStyle = "#aaa";
            context.stroke();

            context.beginPath();
            graph.nodes.forEach(drawNode);
            context.fill();
            context.strokeStyle = "#fff";
            context.stroke();
        }
    }
};
</script>
<style scoped></style>
