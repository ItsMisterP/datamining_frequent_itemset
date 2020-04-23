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
            width: 500,
            height: 500,
            items: []
        };
    },
    mounted() {
        this.init();
    },
    methods: {
        init() {
            var canvas = document.querySelector("canvas"),
            context = canvas.getContext("2d"),
            width = canvas.width,
            height = canvas.height;

            var simulation = d3.forceSimulation()
                .force("link", d3.forceLink().id(function(d) { return d.id; }))
                .force("charge", d3.forceManyBody())
                .force("center", d3.forceCenter(width / 2, height / 2));


            //d3.json("C:\\Studium\\Angewandte_Informatik\\Master\\2te_Semester\\Seminar\\datamining_frequent_itemset\\datamining_frequent_itemset\\website\\src\\assets\\json\\test.json", function(error, graph) {
            let graph = require("../assets/json/test.json")

            simulation
                .nodes(graph.nodes)
                .on("tick", ticked);

            simulation.force("link")
                .links(graph.links);

            d3.select(canvas)
                .call(d3.drag()
                    .container(canvas)
                    .subject(dragsubject)
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            function ticked() {
                context.clearRect(0, 0, width, height);

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

            function dragsubject() {
                return simulation.find(d3.event.x, d3.event.y);
            }

            function dragstarted() {
                if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                d3.event.subject.fx = d3.event.subject.x;
                d3.event.subject.fy = d3.event.subject.y;
                }

                function dragged() {
                d3.event.subject.fx = d3.event.x;
                d3.event.subject.fy = d3.event.y;
                }

                function dragended() {
                if (!d3.event.active) simulation.alphaTarget(0);
                d3.event.subject.fx = null;
                d3.event.subject.fy = null;
                }

                function drawLink(d) {
                context.moveTo(d.source.x, d.source.y);
                context.lineTo(d.target.x, d.target.y);
                }

                function drawNode(d) {
                context.moveTo(d.x + 3, d.y);
                context.arc(d.x, d.y, 3, 0, 2 * Math.PI);
                }
        }
    }
};
</script>
<style scoped></style>
