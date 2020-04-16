<template>
  <div class="content">
    
    <div class="md-layout">

      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Unterschiedliche Attribute</h4>
            <p class="category">Alle Attribute, welche für die Bestimmung der Frequent Itemsets benötigt werden.</p>
          </md-card-header>
          <md-card-content>
            <chart :data="loadedData"></chart>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Items und ihre relative/absolute Anzahl</h4>
            <p class="category">Gibt das Aufkommen der Items an.</p>
          </md-card-header>
          <md-card-content>
            <column></column>
          </md-card-content>
        </md-card>
      
      </div>

      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Unterschiedliche Attribute</h4>
            <p class="category">Alle Attribute, welche für die Bestimmung der Frequent Itemsets benötigt werden.</p>
          </md-card-header>
          <md-card-content>
            <linechart></linechart>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Items und ihre relative/absolute Anzahl</h4>
            <p class="category">Gibt das Aufkommen der Items an.</p>
          </md-card-header>
          <md-card-content>
            <groupedbarchart></groupedbarchart>
          </md-card-content>
        </md-card>
      
      </div>

      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Unterschiedliche Attribute</h4>
            <p class="category">Alle Attribute, welche für die Bestimmung der Frequent Itemsets benötigt werden.</p>
          </md-card-header>
          <md-card-content>
            <multilinechart></multilinechart>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Items und ihre relative/absolute Anzahl</h4>
            <p class="category">Gibt das Aufkommen der Items an.</p>
          </md-card-header>
          <md-card-content>
              <piechart></piechart>
          </md-card-content>
        </md-card>
      
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import Chart from "../components/diagrams/Chart";
import ColumnChart from "../components/diagrams/ColumnChart"
import LineChart from "../components/diagrams/LineChart"
import GroupedBarChart from "../components/diagrams/GroupedBarChart"
import MultiLineChart from "../components/diagrams/MultiLineChart"
import PieChart from "../components/diagrams/PieChart"

export default {
  components: {
    "chart" : Chart,
    "column" : ColumnChart,
    "linechart" : LineChart,
    "groupedbarchart" : GroupedBarChart,
    "multilinechart" : MultiLineChart,
    "piechart" : PieChart
  },
  mounted(){
      console.log("Dashboard mounted... Start importing the data");
      this.fetchData;
  },
  data() {
    return {
        loadedData : {}
    };
  },
  methods:{
    async fetchData(){
        let data = d3.json("");
        this.loadedData = data;
    }
  }
};
</script>
