<template>
  <div class="content">
    
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Verbrechen je nach Tageszeit (grob)</h4>
            <p class="category">Zeigt die absolute Anzahl nach AM und PM an.</p>
          </md-card-header>
          <md-card-content>
            <chart :dataString="this.jsonFiles.crimesByWeekday" id="9"></chart>
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
            <column :data="this.jsonFiles.crimesByTime" id="8"></column>
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
            <column :data="this.jsonFiles.crimesPerBlock" id="7"></column>
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
            <column :data="this.jsonFiles.crimesByLocation" id="6"></column>
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
            <column :data="this.jsonFiles.crimesByPrimaryDescription" id="5"></column>
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
            <column :data="this.jsonFiles.crimesBySecondaryDescription" id="3"></column>
          </md-card-content>
        </md-card>
      
      </div>

      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="gray">
            <h4 class="title">Verbrechen je nach Tageszeit (grob)</h4>
            <p class="category">Zeigt die absolute Anzahl nach AM und PM an.</p>
          </md-card-header>
          <md-card-content>
            <chart :dataString="this.jsonFiles.crimesByDaytime" id="1"></chart>
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
            <column :data="this.jsonFiles.crimesByMonth" id="2"></column>
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
            <linechart :data="this.jsonFiles.crimesPerYear" id="4"></linechart>
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
import test from "../components/diagrams/ZoomableBarChart"

export default {
  components: {
    "chart" : Chart,
    "column" : ColumnChart,
    "linechart" : LineChart,
    "piechart" : PieChart
  },
  created(){
      console.log("Dashboard mounted... Start importing the data");
      this.init();
  },
  data() {
    return {
        loadedData : {},
        jsonFiles:{
          crimesPerYear: Object,
          crimesPerBlock: Object,
          crimesBySecondaryDescription: Object,
          crimesByTime: Object,
          crimesByDaytime: Object,
          crimesByLocation: Object,
          crimesByPrimaryDescription: Object,
        }
    };
  },
  methods:{
    init(){
        this.jsonFiles.crimesPerYear = require('../assets/json/DataframeValueCounts2019.json');
        this.jsonFiles.crimesPerBlock = require('../assets/json/DataframeValueCounts VERNON AVE.json');
        this.jsonFiles.crimesBySecondaryDescription = require('../assets/json/DataframeValueCountsAGG CRIMINAL SEXUAL ABUSE.json');
        this.jsonFiles.crimesByMonth = require('../assets/json/DataframeValueCountsApril.json');
        this.jsonFiles.crimesByWeekday = require("../assets/json/DataframeValueCountsMittwoch.json");
        this.jsonFiles.crimesByTime = require("../assets/json/DataframeValueCounts16.json");
        this.jsonFiles.crimesByDaytime = require("../assets/json/DataframeValueCountsPM.json");
        this.jsonFiles.crimesByLocation = require("../assets/json/DataframeValueCountsSCHOOL - PUBLIC - BUILDING.json");
        this.jsonFiles.crimesByPrimaryDescription = require("../assets/json/DataframeValueCountsSEX OFFENSE.json");        

        console.log(this.jsonFiles.crimesPerBlock)
    },
    async fetchData(){
        let data = d3.json("");
        this.loadedData = data;
    }
  }
};
</script>
