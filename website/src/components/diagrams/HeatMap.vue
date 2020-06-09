
<template>
    <div>
        <svg class="heatmap" :id="id"></svg>
    </div>
</template>

<script>
import { globalStore } from "@/main";
import * as d3 from "d3";
//import * as geoJson from "@/assets/json/boundaries_neighborhoods.json";


export default {
    name: "Test-Chart",
    props: {
        id: String,
        districtCrimeCount: Object
    },
    data() {
        return {
            height: 600,
            width: 600,
            heightSVG: 0,
            widthSVG: 0,
            margin: { top: 30, right: 30, bottom: 30, left: 70 },
            keys: [],
            values: [],
            x0: Object,
            y: Object,
            color: Object,
            svg: Object,
            container: Object,
            line: Object,
            disrictsGeoJson: Object,
            usaGeoJson: Object,
            selectedId: Number,
            selectedPath: Object
        };
    },
    watch: {
        districtCrimeCount: function() {
            //can't test the pre-initialized vue object "disrictsGeoJson" for === undefined, this is the alternative
            if (Object.keys(this.disrictsGeoJson).length === 0) {
                this.fetchGeoData();
            } else {
                this.init();
                this.draw();
            }
        }
    },
    mounted() {
        this.fetchGeoData();
    },
    methods: {
        getURL: function(url) {
            return globalStore.prefix + url;
        },
        fetchGeoData() {
            let diagram = this;

            d3.json(
                this.getURL("json/boundaries_neighborhoods.geo.json")
            ).then(function(data) {
                diagram.disrictsGeoJson = data;
                diagram.init();
                diagram.draw();
            });
        },
        init() {
            this.svg = d3.select(document.getElementById(this.id));
            this.widthSVG = this.width - this.margin.left - this.margin.right;
            this.heightSVG = this.height - this.margin.top - this.margin.bottom;
            this.svg
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 " + this.widthSVG + " " + this.heightSVG);
        },
        draw() {
            //clean the svg slate (https://medium.com/front-end-weekly/remove-all-children-of-the-node-in-javascript-968ad8f120eb)
            this.svg.selectAll("*").remove();
            let diagram = this;
            let colorMin = "#FFF";
            let colorMax = "#F00";
            let lower = 100000;
            let upper = Math.max.apply(
                null,
                Object.values(this.districtCrimeCount)
            );
            let color = d3
                .scaleLinear()
                .domain([lower, upper])
                .range([colorMin, colorMax]);
            // Color gradient legend: https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient
            //Append a defs (for definition) element to your SVG
            let linearGradientHeight = 300;
            var defs = this.svg.append("defs");
            //Append a linearGradient element to the defs and give it a unique id
            var linearGradient = defs
                .append("linearGradient")
                .attr("id", "linear-gradient");
            //Make the gradient horizontal
            linearGradient
                .attr("x1", "0%")
                .attr("y1", "100%")
                .attr("x2", "0%")
                .attr("y2", "0%");
            //Set the color for the start (0%)
            linearGradient
                .append("stop")
                .attr("offset", "0%")
                .attr("stop-color", colorMin); //White
            //Set the color for the end (100%)
            linearGradient
                .append("stop")
                .attr("offset", "100%")
                .attr("stop-color", colorMax); //red
            this.svg
                .append("rect")
                .attr("width", 20)
                .attr("height", linearGradientHeight)
                .attr(
                    "transform",
                    "translate(0, " +
                        (this.height -
                            linearGradientHeight -
                            this.margin.bottom -
                            this.margin.top) +
                        ")"
                )
                .style("fill", "url(#linear-gradient)");
            //Linear gradient labeling
            let stepCount = 5;
            let step = upper / stepCount;
            let vertOffset =
                this.height -
                linearGradientHeight -
                this.margin.bottom -
                this.margin.top +
                10; // + 10 to compensate textsize
            let vertStepOffset = (linearGradientHeight - 10) / stepCount; //-10 to not move the text below svg lower bound
            for (let i = 0; i < stepCount; i++) {
                this.svg
                    .append("text")
                    .text((((stepCount - i) * step) / 1000).toFixed(0) + " K")
                    .attr("x", 30)
                    .attr("y", vertOffset + i * vertStepOffset);
            }
            // Append the 0 separately
            this.svg
                .append("text")
                .text("0")
                .attr("x", 30)
                .attr("y", vertOffset + linearGradientHeight - 10);
            let g = this.svg
                .append("g")
                .attr("class", "svgcontainer")
                .attr("id", "containerid")
                .attr(
                    "transform",
                    "translate(" +
                        this.margin.left +
                        "," +
                        this.margin.top +
                        ")"
                );

            let d = this.disrictsGeoJson.features;
            //http://bl.ocks.org/cjhin/27e01c636dcc0bfa256c7a225971354d
            var center = d3.geoCentroid(this.disrictsGeoJson);
            var scale = 150; //what does this do?
            var projection = d3
                .geoMercator()
                .scale(scale)
                .center(center);
            //Define path generator
            var path = d3.geoPath().projection(projection);

            projection = d3
                .geoMercator()
                .center(center)
                .fitExtent(
                    [
                        [0, 0],
                        [this.width - 180, this.height - 90]
                    ],
                    this.disrictsGeoJson
                );
            path = path.projection(projection);
            //prep the tooltip
            let tooltip = diagram.svg
                .append("g")
                .attr("class", "tooltip")
                .attr("opacity", 0)

            tooltip
                .append("rect")
                .attr("width", 80)
                .attr("height", 37)
                .attr("rx",10)
                .attr("ry",10)
                .attr("fill", "#FFF")
                .style("stroke-width", 1)
                .style("stroke", "#000");
            let tooltext1 = tooltip.append("text").attr("class", "tooltext");
            let tooltext2 = tooltip.append("text").attr("class", "tooltext");
            let paths = g
                .selectAll("path")
                .data(d)
                .enter()
                .append("path")
                .attr("d", path)
                .attr("id", function(d) {
                    return d.properties.sec_neigh;
                })
                .style("fill", function(d, i) {
                    return color(
                        diagram.districtCrimeCount[
                            "ds_" + d.properties.dist_num
                        ]
                    );
                })
                .style("stroke-width", 1)
                .style("stroke", "#FFF")
                .on("mouseover", function(d, i) {
                    d3.select(this)
                        .style("transform", "scale(1.01,1.01)")
                        .style("transform-origin", "50% 50%");
                })
                .on("mouseout", function(d, i) {
                    tooltip.attr("opacity", 0);
                    d3.select(this)
                        .style("transform", "scale(1,1)")
                        .style("transform-origin", "50% 50%");
                })
                .on("click", function(d, i) {
                    if(i !== diagram.selectedId) {
                        d3.select(diagram.selectedDistrict)
                            .style("transform", "scale(1,1)")
                            .style("transform-origin", "50% 50%")
                            .style("stroke-width", 1)
                            .style("stroke", "#FFF");
                    }
                    diagram.selectedId = i;
                    diagram.selectedDistrict = this;
                    d3.select(diagram.selectedDistrict)
                        .style("stroke-width", 2)
                        .style("stroke", "#000")
                        .style("stroke-linecap", "round");

                    //d.properties.dist_label + " district: " + diagram.districtCrimeCount['ds_' + d.properties.dist_num]
                    let point = d3.mouse(this);
                    let x = point[0] + 70;
                    let y = point[1] - 10;
                    //prevent drawing out of the svg box
                    if (x > diagram.widthSVG / 2) {
                        x -= 80;
                    }
                    if (y < diagram.heightSVG / 2) {
                        y += 35;
                    }
                    tooltip
                        .attr("opacity", 1)
                        .attr("transform", "translate(" + x + ", " + y + ")");
                    tooltext1
                        .attr("x", 7)
                        .attr("y", 15)
                        .text(d.properties.dist_label + " district:");
                    tooltext2
                        .attr("x", 7)
                        .attr("y", 30)
                        .text(diagram.districtCrimeCount['ds_' + d.properties.dist_num] + " crimes");
                    diagram.changeSelectedDistrict("ds_" + d.properties.dist_num);
                });
        },
        changeSelectedDistrict(selectedDistrict){
            this.$emit("update-selectedDistrict", selectedDistrict);
        }
    }
};
</script>

<style scoped>

</style>
